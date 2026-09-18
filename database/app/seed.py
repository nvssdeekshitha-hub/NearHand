"""
NEARHAND Database Seed Script
Populates fictional demo data for hackathon presentation and backend integration.
Safe to run multiple times (idempotent).
"""

from datetime import datetime, timezone, timedelta
import json
from sqlalchemy.orm import Session
from app.database import engine, init_db, SessionLocal
import app.models as models
import app.crud as crud


def seed_data():
    init_db()
    db = SessionLocal()
    try:
        # Check if already seeded
        existing_lakshmi = crud.get_user_by_email(db, "lakshmi@nearhand.org")
        if existing_lakshmi:
            print("Database already contains demo seed data. Skipping duplication.")
            return

        print("Seeding NEARHAND database with demo users, seniors, caretakers, volunteers, family, and emergency requests...")

        # ----------------------------------------------------
        # 1. CREATE USERS
        # ----------------------------------------------------

        # Admin
        u_admin = crud.create_user(
            db, name="System Admin", email="admin@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_admin123", role=models.UserRole.ADMIN, phone="+919876543200"
        )

        # Seniors (5 seniors)
        u_lakshmi = crud.create_user(
            db, name="Lakshmi Devi", email="lakshmi@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_senior1", role=models.UserRole.SENIOR, phone="+919876543210"
        )
        u_ramesh = crud.create_user(
            db, name="Ramesh Kumar", email="ramesh@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_senior2", role=models.UserRole.SENIOR, phone="+919876543211"
        )
        u_savitri = crud.create_user(
            db, name="Savitri Amma", email="savitri@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_senior3", role=models.UserRole.SENIOR, phone="+919876543212"
        )
        u_krishna = crud.create_user(
            db, name="Krishna Rao", email="krishna@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_senior4", role=models.UserRole.SENIOR, phone="+919876543213"
        )
        u_padma = crud.create_user(
            db, name="Padma Vati", email="padma@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_senior5", role=models.UserRole.SENIOR, phone="+919876543214"
        )

        # Caretaker (Ravi Kumar)
        u_ravi = crud.create_user(
            db, name="Ravi Kumar", email="ravi.caretaker@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_caretaker1", role=models.UserRole.CARETAKER, phone="+919876543220"
        )

        # Volunteers (Priya Sharma & Rajesh Patel)
        u_priya = crud.create_user(
            db, name="Priya Sharma", email="priya.volunteer@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_volunteer1", role=models.UserRole.VOLUNTEER, phone="+919876543230"
        )
        u_rajesh = crud.create_user(
            db, name="Rajesh Patel", email="rajesh.volunteer@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_volunteer2", role=models.UserRole.VOLUNTEER, phone="+919876543231"
        )

        # Family Member (Anjali)
        u_anjali = crud.create_user(
            db, name="Anjali Devi", email="anjali.family@nearhand.org",
            password_hash="pbkdf2_sha256$mockhash_family1", role=models.UserRole.FAMILY, phone="+919876543240"
        )

        # ----------------------------------------------------
        # 2. CREATE SENIORS TABLE ENTRIES
        # ----------------------------------------------------

        s_lakshmi = crud.create_senior(
            db, user_id=u_lakshmi.id, age=72, gender="Female", preferred_language="Telugu",
            address="Flat 302, Sri Sai Nilayam, MG Road, Vijayawada",
            latitude=16.506, longitude=80.648, home_latitude=16.506, home_longitude=80.648,
            location_deviation_threshold_km=1.0, emergency_contact="+919876543240"
        )

        s_ramesh = crud.create_senior(
            db, user_id=u_ramesh.id, age=75, gender="Male", preferred_language="Hindi",
            address="House 45, Sector 4, Vijayawada",
            latitude=16.510, longitude=80.640, home_latitude=16.510, home_longitude=80.640,
            emergency_contact="+919876543299"
        )

        s_savitri = crud.create_senior(
            db, user_id=u_savitri.id, age=68, gender="Female", preferred_language="Telugu",
            address="Plot 12, Teacher Colony, Vijayawada",
            latitude=16.502, longitude=80.655, home_latitude=16.502, home_longitude=80.655,
            emergency_contact="+919876543298"
        )

        s_krishna = crud.create_senior(
            db, user_id=u_krishna.id, age=80, gender="Male", preferred_language="Telugu",
            address="Flat 101, Krishna Heights, Vijayawada",
            latitude=16.515, longitude=80.650, home_latitude=16.515, home_longitude=80.650,
            emergency_contact="+919876543297"
        )

        s_padma = crud.create_senior(
            db, user_id=u_padma.id, age=70, gender="Female", preferred_language="Telugu",
            address="Door 4-12, Gandhi Nagar, Vijayawada",
            latitude=16.498, longitude=80.642, home_latitude=16.498, home_longitude=80.642,
            emergency_contact="+919876543296"
        )

        # ----------------------------------------------------
        # 3. CREATE CARETAKER & ASSIGN 5 SENIORS TO RAVI
        # ----------------------------------------------------

        caretaker_ravi = crud.create_caretaker(
            db, user_id=u_ravi.id, availability_status=models.AvailabilityStatus.AVAILABLE,
            latitude=16.508, longitude=80.645, max_seniors=5
        )

        # Assign all 5 seniors to Ravi Kumar
        crud.assign_senior_to_caretaker(db, caretaker_id=caretaker_ravi.id, senior_id=s_lakshmi.id, is_primary=True)
        crud.assign_senior_to_caretaker(db, caretaker_id=caretaker_ravi.id, senior_id=s_ramesh.id, is_primary=True)
        crud.assign_senior_to_caretaker(db, caretaker_id=caretaker_ravi.id, senior_id=s_savitri.id, is_primary=True)
        crud.assign_senior_to_caretaker(db, caretaker_id=caretaker_ravi.id, senior_id=s_krishna.id, is_primary=True)
        crud.assign_senior_to_caretaker(db, caretaker_id=caretaker_ravi.id, senior_id=s_padma.id, is_primary=True)

        # ----------------------------------------------------
        # 4. CREATE VOLUNTEERS
        # ----------------------------------------------------

        vol_priya = crud.create_volunteer(
            db, user_id=u_priya.id, latitude=16.520, longitude=80.630, # ~2.4 km from Lakshmi
            availability_status=models.AvailabilityStatus.AVAILABLE,
            max_distance_km=10.0, skills="First Aid, CPR, Elder Mobility Support",
            first_aid_trained=True
        )

        vol_rajesh = crud.create_volunteer(
            db, user_id=u_rajesh.id, latitude=16.500, longitude=80.660,
            availability_status=models.AvailabilityStatus.AVAILABLE,
            max_distance_km=5.0, skills="Grocery assistance, Companion talks",
            first_aid_trained=False
        )

        # ----------------------------------------------------
        # 5. CREATE FAMILY MEMBER RELATIONSHIP
        # ----------------------------------------------------

        fam_anjali = models.FamilyMember(
            user_id=u_anjali.id, senior_id=s_lakshmi.id, relationship="Daughter",
            can_receive_emergency_alerts=True, can_view_health=True, can_view_location=True
        )
        db.add(fam_anjali)
        db.commit()

        # ----------------------------------------------------
        # 6. MEDICAL RECORDS & MEDICATIONS FOR LAKSHMI
        # ----------------------------------------------------

        med_record = models.MedicalRecord(
            senior_id=s_lakshmi.id,
            conditions="Hypertension, Mild Osteoarthritis",
            allergies="Penicillin",
            blood_group="O+",
            important_notes="Prone to sudden dizziness when standing up quickly. Requires low-sodium diet."
        )
        db.add(med_record)

        med1 = models.Medication(
            senior_id=s_lakshmi.id, medicine_name="Amlodipine", dosage="5 mg",
            schedule="8:00 AM - Morning with water", taken_today=True,
            last_taken_at=datetime.now(timezone.utc).replace(hour=8, minute=15)
        )
        med2 = models.Medication(
            senior_id=s_lakshmi.id, medicine_name="Metformin", dosage="500 mg",
            schedule="1:00 PM - Afternoon after lunch", taken_today=True,
            last_taken_at=datetime.now(timezone.utc).replace(hour=13, minute=10)
        )
        med3 = models.Medication(
            senior_id=s_lakshmi.id, medicine_name="Atorvastatin", dosage="10 mg",
            schedule="8:00 PM - Evening before sleep", taken_today=False
        )
        db.add_all([med1, med2, med3])
        db.commit()

        # ----------------------------------------------------
        # 7. DEMO FALL EMERGENCY REQUEST (LAKSHMI)
        # ----------------------------------------------------

        ai_analysis_payload = {
            "language": "Telugu",
            "language_code": "te",
            "transcript": "Nenu bathroom lo padipoyanu, levalekapothunnanu.",
            "normalized_text": "I fell down in the bathroom and I am unable to get up.",
            "request_type": "FALL",
            "urgency": "CRITICAL",
            "risk_score": 94,
            "emergency": True,
            "potential_emergency": True,
            "fall_detected": True,
            "mobility_issue": True,
            "medical_attention_possible": True,
            "companionship": False,
            "location_relevant": True,
            "location_context": "Bathroom, Home",
            "required_support": "Immediate physical assistance and medical fall evaluation",
            "explanation": "Senior explicitly reported falling in the bathroom and inability to rise. High risk of physical injury.",
            "confidence": 0.96
        }

        demo_req = crud.create_request(
            db,
            senior_id=s_lakshmi.id,
            message="Nenu bathroom lo padipoyanu, levalekapothunnanu.",
            input_type=models.InputType.AUDIO,
            language="Telugu",
            request_type=models.RequestType.FALL,
            urgency=models.UrgencyLevel.CRITICAL,
            risk_score=94,
            emergency=True,
            potential_emergency=True,
            fall_detected=True,
            mobility_issue=True,
            medical_attention_possible=True,
            required_support="Immediate physical assistance and medical evaluation",
            location_relevant=True,
            location_context="Bathroom, Home",
            companionship=False,
            status=models.RequestStatus.CARETAKER_NOTIFIED,
            target_response_minutes=2,
            ai_analysis_json=json.dumps(ai_analysis_payload)
        )

        # ----------------------------------------------------
        # 8. DEMO ASSIGNMENT & ESCALATION TRAIL
        # ----------------------------------------------------

        # Caretaker initial assignment (timed out)
        assign_ravi = crud.create_assignment(
            db,
            request_id=demo_req.id,
            responder_type=models.ResponderType.CARETAKER,
            responder_id=u_ravi.id,
            assignment_status=models.AssignmentStatus.TIMEOUT,
            distance_km=0.5,
            eta_minutes=4,
            response_deadline=datetime.now(timezone.utc) + timedelta(minutes=2)
        )

        # Volunteer assignment (accepted)
        assign_priya = crud.create_assignment(
            db,
            request_id=demo_req.id,
            responder_type=models.ResponderType.VOLUNTEER,
            responder_id=u_priya.id,
            assignment_status=models.AssignmentStatus.ACCEPTED,
            distance_km=2.4,
            eta_minutes=7
        )
        assign_priya.accepted_at = datetime.now(timezone.utc)

        # Update request status to reflect volunteer acceptance & family notification
        crud.update_request_status(db, request_id=demo_req.id, status=models.RequestStatus.VOLUNTEER_ACCEPTED)

        # ----------------------------------------------------
        # 9. DEMO NOTIFICATIONS
        # ----------------------------------------------------

        crud.create_notification(
            db, user_id=u_ravi.id, request_id=demo_req.id,
            notification_type=models.NotificationType.EMERGENCY,
            title="CRITICAL FALL ALERT: Lakshmi Devi",
            message="Lakshmi reported a fall in the bathroom. Target response: 2 mins."
        )

        crud.create_notification(
            db, user_id=u_priya.id, request_id=demo_req.id,
            notification_type=models.NotificationType.ESCALATION,
            title="VOLUNTEER REQUEST: Nearby Senior Needs Help",
            message="Caretaker timeout. Lakshmi Devi (2.4 km away) requires fall assistance."
        )

        crud.create_notification(
            db, user_id=u_anjali.id, request_id=demo_req.id,
            notification_type=models.NotificationType.FAMILY,
            title="FAMILY ALERT: Emergency Notification for Lakshmi",
            message="Fall alert registered for Lakshmi. Volunteer Priya Sharma has accepted and is en route."
        )

        # ----------------------------------------------------
        # 10. DEMO LOCATION EVENT (DEVIATION DEMO)
        # ----------------------------------------------------

        crud.create_location_event(
            db, senior_id=s_lakshmi.id,
            latitude=16.535, longitude=80.680,
            distance_from_home_km=4.5,
            deviation_detected=True, expected_trip=False
        )

        # ----------------------------------------------------
        # 11. AUDIT LOG INITIALIZATION
        # ----------------------------------------------------

        crud.create_audit_log(
            db, action="REQUEST_CREATED", entity_type="Request",
            user_id=u_lakshmi.id, entity_id=str(demo_req.id),
            details="Senior triggered critical fall emergency request in Telugu."
        )
        crud.create_audit_log(
            db, action="CARETAKER_TIMEOUT", entity_type="Assignment",
            user_id=u_ravi.id, entity_id=str(assign_ravi.id),
            details="Caretaker Ravi Kumar did not respond within 2-minute deadline."
        )
        crud.create_audit_log(
            db, action="VOLUNTEER_ASSIGNED", entity_type="Assignment",
            user_id=u_priya.id, entity_id=str(assign_priya.id),
            details="Volunteer Priya Sharma accepted request fallback."
        )

        print("NEARHAND database seed successfully completed!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
