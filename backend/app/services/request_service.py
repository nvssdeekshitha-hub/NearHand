from datetime import datetime, timedelta, timezone
import json
import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import (
    Request, Assignment, Senior, Caretaker, CaretakerSenior,
    RequestStatus, RequestUrgency, ResponderType, AssignmentStatus
)
from app.schemas.request import RequestCreate
from app.services.ai_service import analyze_text_request
from app.services.notification_service import create_notification
from app.services.escalation_service import notify_family_members
from app.api.websocket import emit_ws_event
from app.utils.distance import haversine_distance, estimate_eta_minutes

logger = logging.getLogger(__name__)

def get_target_response_minutes(urgency: str) -> int:
    urgency_upper = urgency.upper() if urgency else "MEDIUM"
    if urgency_upper == RequestUrgency.CRITICAL.value:
        return settings.TARGET_RESPONSE_CRITICAL
    elif urgency_upper == RequestUrgency.HIGH.value:
        return settings.TARGET_RESPONSE_HIGH
    elif urgency_upper == RequestUrgency.MEDIUM.value:
        return settings.TARGET_RESPONSE_MEDIUM
    else:
        return settings.TARGET_RESPONSE_LOW

def create_and_process_request(db: Session, request_in: RequestCreate, senior: Senior) -> Request:
    """
    Core request orchestration flow:
    1. Create request with status ANALYZING
    2. Emit REQUEST_CREATED WS event to senior
    3. Run AI text analysis (with fallback)
    4. Emit AI_ANALYSIS_COMPLETE WS event to senior
    5. Calculate target response window & set status PRIORITIZED
    6. Handle emergency or assign primary caretaker & emit CARETAKER_NOTIFIED
    """
    # Create initial request record
    req = Request(
        senior_id=senior.id,
        message=request_in.message,
        input_type=request_in.input_type or "TEXT",
        status=RequestStatus.ANALYZING.value
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    # 1. Emit WS Event: REQUEST_CREATED (to senior user_id)
    logger.info(f"[REQUEST SERVICE] Preparing to emit REQUEST_CREATED for Senior ID={senior.id}, User ID={senior.user_id}")
    emit_ws_event(
        user_id=senior.user_id,
        event_name="REQUEST_CREATED",
        data={
            "request_id": req.id,
            "senior_id": senior.id,
            "message": req.message,
            "input_type": req.input_type,
            "status": req.status
        }
    )
    logger.info(f"[REQUEST SERVICE] Emitted REQUEST_CREATED to User ID={senior.user_id}")

    # Run AI Analysis
    ai_result = analyze_text_request(request_in.message)

    # Populate request metadata
    req.language = ai_result.language
    req.request_type = ai_result.request_type
    req.urgency = ai_result.urgency
    req.risk_score = ai_result.risk_score
    req.emergency = ai_result.emergency
    req.required_support = json.dumps(ai_result.required_support)
    req.companionship = (ai_result.request_type == "COMPANIONSHIP")

    # Calculate target response window
    req.target_response_minutes = get_target_response_minutes(ai_result.urgency)
    req.status = RequestStatus.PRIORITIZED.value
    db.commit()
    db.refresh(req)

    # 2. Emit WS Event: AI_ANALYSIS_COMPLETE (to senior user_id)
    logger.info(f"[REQUEST SERVICE] Preparing to emit AI_ANALYSIS_COMPLETE for Senior ID={senior.id}, User ID={senior.user_id}")
    emit_ws_event(
        user_id=senior.user_id,
        event_name="AI_ANALYSIS_COMPLETE",
        data={
            "request_id": req.id,
            "senior_id": senior.id,
            "language": req.language,
            "request_type": req.request_type,
            "urgency": req.urgency,
            "risk_score": req.risk_score,
            "emergency": req.emergency,
            "target_response_minutes": req.target_response_minutes
        }
    )
    logger.info(f"[REQUEST SERVICE] Emitted AI_ANALYSIS_COMPLETE to User ID={senior.user_id}")

    # Check for primary caretaker
    primary_link = db.query(CaretakerSenior).filter(
        CaretakerSenior.senior_id == senior.id,
        CaretakerSenior.is_primary == True
    ).first()

    caretaker = None
    if primary_link:
        caretaker = db.query(Caretaker).filter(Caretaker.id == primary_link.caretaker_id).first()

    if ai_result.emergency:
        # Emergency SOS bypass flow
        req.status = RequestStatus.CARETAKER_NOTIFIED.value
        db.commit()

        if caretaker:
            # Create urgent assignment
            dist_km = 1.0
            if caretaker.latitude and caretaker.longitude and senior.latitude and senior.longitude:
                dist_km = haversine_distance(caretaker.latitude, caretaker.longitude, senior.latitude, senior.longitude)
            
            assignment = Assignment(
                request_id=req.id,
                responder_type=ResponderType.CARETAKER.value,
                responder_id=caretaker.id,
                assignment_status=AssignmentStatus.PENDING.value,
                assigned_at=datetime.now(timezone.utc),
                response_deadline=datetime.now(timezone.utc) + timedelta(minutes=req.target_response_minutes),
                distance_km=dist_km,
                eta_minutes=estimate_eta_minutes(dist_km)
            )
            db.add(assignment)
            db.commit()

            # 3. Emit WS Event: CARETAKER_NOTIFIED (via create_notification)
            create_notification(
                db=db,
                user_id=caretaker.user_id,
                notification_type="CARETAKER_NOTIFIED",
                title="EMERGENCY ALERT",
                message=f"CRITICAL emergency for Senior ID {senior.id}: {request_in.message}",
                request_id=req.id
            )

        # Immediately notify family members too (Emits FAMILY_NOTIFIED WS events)
        notify_family_members(
            db=db,
            senior_id=senior.id,
            request_id=req.id,
            title="EMERGENCY ALERT NOTIFICATION",
            message=f"Emergency request initiated by senior: {request_in.message}"
        )
        
        req.status = RequestStatus.WAITING_FOR_ACKNOWLEDGEMENT.value
        db.commit()
        db.refresh(req)

    else:
        # Normal escalation flow via Caretaker
        if caretaker:
            dist_km = 1.0
            if caretaker.latitude and caretaker.longitude and senior.latitude and senior.longitude:
                dist_km = haversine_distance(caretaker.latitude, caretaker.longitude, senior.latitude, senior.longitude)

            deadline = datetime.now(timezone.utc) + timedelta(minutes=req.target_response_minutes)
            
            assignment = Assignment(
                request_id=req.id,
                responder_type=ResponderType.CARETAKER.value,
                responder_id=caretaker.id,
                assignment_status=AssignmentStatus.PENDING.value,
                assigned_at=datetime.now(timezone.utc),
                response_deadline=deadline,
                distance_km=dist_km,
                eta_minutes=estimate_eta_minutes(dist_km)
            )
            db.add(assignment)
            
            req.status = RequestStatus.CARETAKER_NOTIFIED.value
            db.commit()

            # 3. Emit WS Event: CARETAKER_NOTIFIED (via create_notification)
            create_notification(
                db=db,
                user_id=caretaker.user_id,
                notification_type="CARETAKER_NOTIFIED",
                title="New Support Request",
                message=f"Request from Senior ID {senior.id}: {request_in.message}",
                request_id=req.id
            )

            req.status = RequestStatus.WAITING_FOR_ACKNOWLEDGEMENT.value
            db.commit()
            db.refresh(req)

        else:
            # If no caretaker, attempt volunteer match directly
            from app.services.escalation_service import handle_caretaker_timeout
            handle_caretaker_timeout(db=db, request_id=req.id)

    return req
