import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.database import Base
import app.models as models
import app.crud as crud
import app.relationships  # Ensure relationship bindings


@pytest.fixture(scope="function")
def db_session():
    """Create an in-memory SQLite database session for each test function."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    
    # Enable foreign key enforcement for SQLite in-memory DB
    from sqlalchemy import event
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


# ==========================================
# 1. USER TESTS & UNIQUE CONSTRAINTS
# ==========================================

def test_create_user(db_session):
    user = crud.create_user(
        db_session,
        name="Test Senior",
        email="test.senior@example.com",
        password_hash="hashed_pw_123",
        role=models.UserRole.SENIOR,
        phone="+919999999999"
    )
    assert user.id is not None
    assert user.email == "test.senior@example.com"
    assert user.role == models.UserRole.SENIOR

    fetched = crud.get_user_by_email(db_session, "test.senior@example.com")
    assert fetched is not None
    assert fetched.id == user.id


def test_duplicate_user_email_fails(db_session):
    crud.create_user(
        db_session,
        name="User 1",
        email="unique@example.com",
        password_hash="pw1",
        role=models.UserRole.SENIOR
    )
    with pytest.raises(IntegrityError):
        crud.create_user(
            db_session,
            name="User 2",
            email="unique@example.com",
            password_hash="pw2",
            role=models.UserRole.VOLUNTEER
        )


# ==========================================
# 2. SENIOR & CARETAKER ASSIGNMENT (5 SENIORS -> 1 CARETAKER)
# ==========================================

def test_senior_and_caretaker_assignment(db_session):
    # Create Caretaker User & Caretaker Record
    ct_user = crud.create_user(
        db_session, name="Ravi Caretaker", email="ravi@example.com",
        password_hash="pw", role=models.UserRole.CARETAKER
    )
    caretaker = crud.create_caretaker(db_session, user_id=ct_user.id, max_seniors=5)

    seniors = []
    for i in range(5):
        s_user = crud.create_user(
            db_session, name=f"Senior {i+1}", email=f"senior{i+1}@example.com",
            password_hash="pw", role=models.UserRole.SENIOR
        )
        senior = crud.create_senior(
            db_session, user_id=s_user.id, age=70+i, preferred_language="Telugu",
            latitude=16.5, longitude=80.6
        )
        crud.assign_senior_to_caretaker(db_session, caretaker_id=caretaker.id, senior_id=senior.id)
        seniors.append(senior)

    # Verify Caretaker has 5 assigned seniors
    ct_seniors = crud.get_caretaker_seniors(db_session, caretaker.id)
    assert len(ct_seniors) == 5
    assert caretaker.current_load == 5

    # Verify primary caretaker lookup for Senior 1
    retrieved_ct = crud.get_senior_caretaker(db_session, seniors[0].id)
    assert retrieved_ct is not None
    assert retrieved_ct.id == caretaker.id


# ==========================================
# 3. VOLUNTEER & LOCATION DISTANCE QUERY
# ==========================================

def test_volunteer_creation_and_nearby_search(db_session):
    v_user = crud.create_user(
        db_session, name="Priya Volunteer", email="priya@example.com",
        password_hash="pw", role=models.UserRole.VOLUNTEER
    )
    volunteer = crud.create_volunteer(
        db_session, user_id=v_user.id, latitude=16.520, longitude=80.630,
        availability_status=models.AvailabilityStatus.AVAILABLE,
        max_distance_km=10.0, first_aid_trained=True
    )

    available = crud.get_available_volunteers(db_session)
    assert len(available) == 1
    assert available[0].first_aid_trained is True

    # Search near (16.506, 80.648)
    nearby = crud.get_volunteers_near_location(db_session, latitude=16.506, longitude=80.648, max_distance_km=5.0)
    assert len(nearby) == 1
    assert nearby[0].id == volunteer.id


# ==========================================
# 4. FAMILY MEMBERSHIP & HEALTH PRIVACY
# ==========================================

def test_family_member_relationships(db_session):
    s_user = crud.create_user(db_session, name="Senior Lakshmi", email="lakshmi@example.com", password_hash="pw", role=models.UserRole.SENIOR)
    senior = crud.create_senior(db_session, user_id=s_user.id, age=72)

    f_user = crud.create_user(db_session, name="Anjali Daughter", email="anjali@example.com", password_hash="pw", role=models.UserRole.FAMILY)
    
    fam = models.FamilyMember(
        user_id=f_user.id, senior_id=senior.id, relationship="Daughter",
        can_receive_emergency_alerts=True, can_view_health=True, can_view_location=True
    )
    db_session.add(fam)
    db_session.commit()

    family_list = crud.get_senior_family(db_session, senior.id)
    assert len(family_list) == 1
    assert family_list[0].relationship == "Daughter"
    assert family_list[0].can_view_health is True


# ==========================================
# 5. MEDICAL RECORDS & MEDICATIONS
# ==========================================

def test_medical_records_and_medications(db_session):
    s_user = crud.create_user(db_session, name="Senior Med", email="seniormed@example.com", password_hash="pw", role=models.UserRole.SENIOR)
    senior = crud.create_senior(db_session, user_id=s_user.id, age=72)

    rec = models.MedicalRecord(senior_id=senior.id, conditions="Hypertension", allergies="Penicillin", blood_group="O+")
    med = models.Medication(senior_id=senior.id, medicine_name="Amlodipine", dosage="5 mg", schedule="8:00 AM", taken_today=True)
    db_session.add_all([rec, med])
    db_session.commit()

    health_info = crud.get_senior_health(db_session, senior.id)
    assert len(health_info["medical_records"]) == 1
    assert len(health_info["medications"]) == 1
    assert health_info["medications"][0].medicine_name == "Amlodipine"
    assert health_info["medications"][0].taken_today is True


# ==========================================
# 6. REQUEST CREATION & RISK SCORE VALIDATION
# ==========================================

def test_request_creation_and_workflow(db_session):
    s_user = crud.create_user(db_session, name="Senior Fall", email="seniorfall@example.com", password_hash="pw", role=models.UserRole.SENIOR)
    senior = crud.create_senior(db_session, user_id=s_user.id, age=72)

    req = crud.create_request(
        db_session,
        senior_id=senior.id,
        message="Nenu bathroom lo padipoyanu",
        input_type=models.InputType.AUDIO,
        language="Telugu",
        request_type=models.RequestType.FALL,
        urgency=models.UrgencyLevel.CRITICAL,
        risk_score=94,
        emergency=True,
        fall_detected=True,
        target_response_minutes=2,
        status=models.RequestStatus.CARETAKER_NOTIFIED
    )

    assert req.id is not None
    assert req.risk_score == 94
    assert req.fall_detected is True
    assert req.status == models.RequestStatus.CARETAKER_NOTIFIED

    # Update status to RESOLVED
    updated = crud.update_request_status(db_session, req.id, status=models.RequestStatus.RESOLVED)
    assert updated.status == models.RequestStatus.RESOLVED
    assert updated.resolved_at is not None


# ==========================================
# 7. ASSIGNMENT & NOTIFICATION CREATION
# ==========================================

def test_assignment_and_notifications(db_session):
    s_user = crud.create_user(db_session, name="Senior Req", email="seniorreq@example.com", password_hash="pw", role=models.UserRole.SENIOR)
    senior = crud.create_senior(db_session, user_id=s_user.id, age=72)

    r_user = crud.create_user(db_session, name="Responder Caretaker", email="responder@example.com", password_hash="pw", role=models.UserRole.CARETAKER)
    
    req = crud.create_request(db_session, senior_id=senior.id, message="Need medical help", urgency=models.UrgencyLevel.HIGH)

    assignment = crud.create_assignment(
        db_session,
        request_id=req.id,
        responder_type=models.ResponderType.CARETAKER,
        responder_id=r_user.id,
        assignment_status=models.AssignmentStatus.PENDING,
        distance_km=1.2,
        eta_minutes=5
    )

    assert assignment.id is not None
    assert assignment.distance_km == 1.2

    # Accept assignment
    updated_assign = crud.update_assignment(db_session, assignment.id, models.AssignmentStatus.ACCEPTED)
    assert updated_assign.assignment_status == models.AssignmentStatus.ACCEPTED
    assert updated_assign.accepted_at is not None

    # Create Notification
    notif = crud.create_notification(
        db_session, user_id=r_user.id, request_id=req.id,
        notification_type=models.NotificationType.EMERGENCY,
        title="Emergency", message="Emergency alert!"
    )
    assert notif.is_read is False

    user_notifs = crud.get_user_notifications(db_session, r_user.id, unread_only=True)
    assert len(user_notifs) == 1

    read_notif = crud.mark_notification_read(db_session, notif.id)
    assert read_notif.is_read is True


# ==========================================
# 8. LOCATION EVENTS & COMPANIONSHIP
# ==========================================

def test_location_event_and_companionship(db_session):
    s_user = crud.create_user(db_session, name="Senior Loc", email="seniorloc@example.com", password_hash="pw", role=models.UserRole.SENIOR)
    senior = crud.create_senior(db_session, user_id=s_user.id, age=72)

    loc = crud.create_location_event(
        db_session, senior_id=senior.id, latitude=16.535, longitude=80.680,
        distance_from_home_km=4.5, deviation_detected=True
    )
    assert loc.deviation_detected is True

    latest = crud.get_latest_location(db_session, senior.id)
    assert latest.latitude == 16.535

    req = crud.create_request(db_session, senior_id=senior.id, message="Looking for someone to talk to", request_type=models.RequestType.COMPANIONSHIP)
    comp = models.CompanionshipRequest(senior_id=senior.id, request_id=req.id, status=models.CompanionshipStatus.REQUESTED)
    db_session.add(comp)
    db_session.commit()

    assert comp.id is not None
    assert comp.status == models.CompanionshipStatus.REQUESTED
