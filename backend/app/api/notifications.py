from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Notification
from app.schemas.common import success_response, error_response

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/{user_id}")
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(Notification.id.desc()).all()

    results = []
    for n in notifications:
        results.append({
            "id": n.id,
            "user_id": n.user_id,
            "request_id": n.request_id,
            "type": n.type,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat() if n.created_at else None
        })

    return success_response(data=results, message="Notifications retrieved")

@router.patch("/{id}/read")
def mark_notification_read(id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == id).first()
    if not notif:
        raise HTTPException(status_code=404, detail=error_response("NOT_FOUND", f"Notification {id} not found."))

    notif.is_read = True
    db.commit()
    return success_response(
        data={"id": notif.id, "is_read": True},
        message="Notification marked as read"
    )
