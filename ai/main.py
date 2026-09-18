from priority import get_priority
from matching import find_caregiver
from reassignment import reassign_caregiver


# Caregiver data
caregivers = [
    {
        "id": "C01",
        "availability": "Available",
        "skill": "Medical",
        "eta": 10
    },
    {
        "id": "C02",
        "availability": "Available",
        "skill": "Medical",
        "eta": 7
    },
    {
        "id": "C03",
        "availability": "Available",
        "skill": "General",
        "eta": 12
    }
]


# Senior request
request_type = "Medical"
urgency = "High"


# Step 1: Find priority
priority = get_priority(request_type, urgency)

print("===== NEARHAND AI =====")
print("Request Type:", request_type)
print("Priority:", priority)


# Step 2: Find caregiver
caregiver = find_caregiver(caregivers, request_type)

if caregiver:

    print("Recommended Caregiver:", caregiver["id"])
    print("ETA:", caregiver["eta"], "minutes")

    print("\nReason:")
    print("- Caregiver is available")
    print("- Required skill matched")
    print("- Fast response time")

    # Step 3: Simulate rejection
    print("\nCaregiver", caregiver["id"], "rejected the request.")

    new_caregiver = reassign_caregiver(
        caregivers,
        request_type,
        caregiver["id"]
    )

    if new_caregiver:
        print("\n===== AUTOMATIC REASSIGNMENT =====")
        print("New Caregiver:", new_caregiver["id"])
        print("ETA:", new_caregiver["eta"], "minutes")
        print("Reason: Automatically reassigned")
    else:
        print("No alternative caregiver available.")

else:
    print("No suitable caregiver available.")