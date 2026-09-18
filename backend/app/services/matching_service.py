import json
import logging
from typing import List, Tuple, Dict, Any
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Volunteer, User, Senior, Request, RequestType, RequestUrgency
from app.utils.distance import haversine_distance, estimate_eta_minutes

logger = logging.getLogger(__name__)

def score_volunteer(
    volunteer: Volunteer,
    senior_lat: float,
    senior_lon: float,
    request: Request
) -> Tuple[float, float, int]:
    """
    Computes weighted score for a volunteer relative to a senior's request.
    Returns (total_score, distance_km, eta_minutes).
    Weights:
    - 40% urgency-sensitivity
    - 25% estimated response time
    - 15% distance
    - 10% availability
    - 10% skill match
    """
    dist_km = haversine_distance(volunteer.latitude, volunteer.longitude, senior_lat, senior_lon)
    eta = estimate_eta_minutes(dist_km)

    # 1. Distance Score (0 to 100): 100 at 0km, decreases linearly up to max_distance_km
    max_radius = max(volunteer.max_distance_km, settings.VOLUNTEER_SEARCH_RADIUS_KM)
    distance_score = max(0.0, 100.0 * (1.0 - (dist_km / max_radius)))

    # 2. ETA Score (0 to 100): 100 if ETA <= 5 min, decreases for longer ETA
    eta_score = max(0.0, 100.0 * (1.0 - (min(eta, 60) / 60.0)))

    # 3. Urgency Sensitivity (0 to 100): higher score for critical requests
    urgency_map = {
        RequestUrgency.CRITICAL.value: 100.0,
        RequestUrgency.HIGH.value: 80.0,
        RequestUrgency.MEDIUM.value: 50.0,
        RequestUrgency.LOW.value: 30.0,
    }
    urgency_score = urgency_map.get(request.urgency, 50.0)

    # 4. Availability Score (0 to 100)
    availability_score = 100.0 if volunteer.availability_status else 0.0

    # 5. Skill Match Score (0 to 100)
    skill_score = 50.0
    if volunteer.first_aid_trained and request.request_type in [RequestType.FALL.value, RequestType.MEDICAL_HELP.value, RequestType.EMERGENCY.value]:
        skill_score = 100.0

    # Calculate final weighted score
    total_score = (
        (settings.WEIGHT_URGENCY * urgency_score) +
        (settings.WEIGHT_ETA * eta_score) +
        (settings.WEIGHT_DISTANCE * distance_score) +
        (settings.WEIGHT_AVAILABILITY * availability_score) +
        (settings.WEIGHT_SKILL * skill_score)
    )

    return (round(total_score, 2), dist_km, eta)

def find_best_volunteers(
    db: Session,
    senior: Senior,
    request: Request,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Queries active volunteers within radius and returns top candidates sorted by score.
    """
    if senior.latitude is None or senior.longitude is None:
        senior_lat, senior_lon = 17.385044, 78.486671
    else:
        senior_lat, senior_lon = senior.latitude, senior.longitude

    volunteers = db.query(Volunteer).filter(Volunteer.availability_status == True).all()

    candidates = []
    for vol in volunteers:
        score, dist_km, eta = score_volunteer(vol, senior_lat, senior_lon, request)
        if dist_km <= max(vol.max_distance_km, settings.VOLUNTEER_SEARCH_RADIUS_KM):
            user = db.query(User).filter(User.id == vol.user_id).first()
            user_name = user.name if user else "Volunteer"
            try:
                skills_list = json.loads(vol.skills) if vol.skills else []
            except Exception:
                skills_list = ["First Aid"] if vol.first_aid_trained else []

            candidates.append({
                "volunteer_id": vol.id,
                "user_id": vol.user_id,
                "name": user_name,
                "distance_km": dist_km,
                "eta_minutes": eta,
                "score": score,
                "available": vol.availability_status,
                "skills": skills_list,
                "first_aid_trained": vol.first_aid_trained,
                "volunteer_obj": vol
            })

    # Sort candidates by score descending
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:limit]
