import json
import logging
from sqlalchemy.orm import Session

from app.db.database import SessionLocal, engine, Base
from app.db.models import (
    User, Senior, Caretaker, CaretakerSenior, Volunteer, Family,
    MedicalRecord, Medication, UserRole
)
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

def seed_data(db: Session):
    logger.info("Dropping and recreating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    password_hash = get_password_hash("password123")

    # 1. Create Caretaker User (Ravi Kumar)
    ravi_user = User(
        name="Ravi Kumar",
        email="ravi@nearhand.com",
        phone="+919876543210",
        password_hash=password_hash,
        role=UserRole.CARETAKER.value
    )
    db.add(ravi_user)
    db.flush()

    ravi_caretaker = Caretaker(
        user_id=ravi_user.id,
        availability_status=True,
        latitude=17.385044,
        longitude=78.486671,
        max_seniors=10,
        current_load=5
    )
    db.add(ravi_caretaker)
    db.flush()

    # 2. Create Senior 1: Lakshmi (Primary Hero Demo Senior)
    lakshmi_user = User(
        name="Lakshmi",
        email="senior@nearhand.com",
        phone="+919123456780",
        password_hash=password_hash,
        role=UserRole.SENIOR.value
    )
    db.add(lakshmi_user)
    db.flush()

    lakshmi_senior = Senior(
        user_id=lakshmi_user.id,
        age=72,
        gender="Female",
        preferred_language="Telugu",
        address="Banjara Hills, Hyderabad",
        latitude=17.4126,
        longitude=78.4482,
        home_latitude=17.4126,
        home_longitude=78.4482,
        location_deviation_threshold_km=1.0,
        emergency_contact="+919988776655"
    )
    db.add(lakshmi_senior)
    db.flush()

    # Link Lakshmi to Ravi
    db.add(CaretakerSenior(caretaker_id=ravi_caretaker.id, senior_id=lakshmi_senior.id, is_primary=True))

    # Lakshmi Medical Record
    db.add(MedicalRecord(
        senior_id=lakshmi_senior.id,
        conditions="Hypertension, Mild Arthritis",
        allergies="Penicillin",
        blood_group="O+",
        important_notes="History of dizziness when standing up quickly. Requires assistance for heavy walking."
    ))

    # Lakshmi Medications
    db.add(Medication(senior_id=lakshmi_senior.id, medicine_name="Amlodipine", dosage="5mg", schedule="Morning 8:00 AM", taken_today=True))
    db.add(Medication(senior_id=lakshmi_senior.id, medicine_name="Paracetamol", dosage="500mg", schedule="As needed for joint pain", taken_today=False))

    # 3. Create Family Member: Anjali
    anjali_user = User(
        name="Anjali",
        email="family@nearhand.com",
        phone="+919988776655",
        password_hash=password_hash,
        role=UserRole.FAMILY.value
    )
    db.add(anjali_user)
    db.flush()

    db.add(Family(
        user_id=anjali_user.id,
        senior_id=lakshmi_senior.id,
        relationship="Daughter",
        can_receive_emergency_alerts=True,
        can_view_health=True,
        can_view_location=True
    ))

    # 4. Create Volunteer: Priya Sharma (~2.4km from Lakshmi)
    # Lakshmi is at (17.4126, 78.4482). Priya at (17.4260, 78.4620) is ~2.4km
    priya_user = User(
        name="Priya Sharma",
        email="volunteer@nearhand.com",
        phone="+919443322110",
        password_hash=password_hash,
        role=UserRole.VOLUNTEER.value
    )
    db.add(priya_user)
    db.flush()

    priya_volunteer = Volunteer(
        user_id=priya_user.id,
        latitude=17.4260,
        longitude=78.4620,
        availability_status=True,
        max_distance_km=5.0,
        skills=json.dumps(["First Aid", "CPR Trained", "Telugu Speaker"]),
        first_aid_trained=True,
        current_active_requests=0
    )
    db.add(priya_volunteer)

    # 5. Create 4 Additional Seniors assigned to Ravi Kumar (Total 5 Seniors for Ravi)
    other_seniors_data = [
        ("Ramesh V.", "ramesh@nearhand.com", 75, "Male", "Hypertension", "Apospirin", 17.4150, 78.4450),
        ("Sunita Rao", "sunita@nearhand.com", 69, "Female", "Diabetes Type 2", "Metformin", 17.4110, 78.4500),
        ("Gopal K.", "gopal@nearhand.com", 81, "Male", "Osteoarthritis", "Calcirol", 17.4080, 78.4420),
        ("Kamala Devi", "kamala@nearhand.com", 74, "Female", "Asthma", "Inhaler", 17.4180, 78.4520),
    ]

    for name, email, age, gender, cond, med_name, lat, lon in other_seniors_data:
        u = User(name=name, email=email, phone="+919000000000", password_hash=password_hash, role=UserRole.SENIOR.value)
        db.add(u)
        db.flush()
        s = Senior(
            user_id=u.id, age=age, gender=gender, preferred_language="Telugu",
            address="Hyderabad, India", latitude=lat, longitude=lon, home_latitude=lat, home_longitude=lon
        )
        db.add(s)
        db.flush()
        db.add(CaretakerSenior(caretaker_id=ravi_caretaker.id, senior_id=s.id, is_primary=True))
        db.add(MedicalRecord(senior_id=s.id, conditions=cond, allergies="None", blood_group="B+", important_notes="Regular checkups."))
        db.add(Medication(senior_id=s.id, medicine_name=med_name, dosage="10mg", schedule="Daily morning"))

    db.commit()
    logger.info("Database seeding completed successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
