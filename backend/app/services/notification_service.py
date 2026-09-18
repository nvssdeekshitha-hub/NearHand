import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.db.models import Notification
from app.api.websocket import emit_ws_event

logger = logging.getLogger(__name__)

def create_notification(
    db: Session,
    user_id: int,
    notification_type: str,
    title: str,
    message: str,
    request_id: Optional[int] = None,
    extra_data: Optional[dict] = None
) -> Notification:
    """
    Creates and persists a notification record in database, and broadcasts WebSocket event.
    """
    notif = Notification(
        user_id=user_id,
        request_id=request_id,
        type=notification_type,
        title=title,
        message=message,
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)

    logger.info(f"NOTIFICATION to User {user_id} [{notification_type}]: {title} - {message}")

    # Emit real-time WebSocket event
    event_data = {
        "notification_id": notif.id,
        "request_id": request_id,
        "title": title,
        "message": message,
        "user_id": user_id
    }
    if extra_data:
        event_data.update(extra_data)

    emit_ws_event(user_id=user_id, event_name=notification_type, data=event_data)

    return notif
