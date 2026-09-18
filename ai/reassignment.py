def reassign_caregiver(caregivers, request_type, rejected_id):

    suitable = []

    for caregiver in caregivers:

        if caregiver["id"] != rejected_id and \
           caregiver["availability"] == "Available" and \
           caregiver["skill"] == request_type:

            suitable.append(caregiver)

    if not suitable:
        return None

    # Select the caregiver with the lowest ETA
    best = min(suitable, key=lambda x: x["eta"])

    return best


# Sample caregiver data
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
        "skill": "Medical",
        "eta": 12
    }
]


# C02 rejected the request
rejected_caregiver = "C02"

result = reassign_caregiver(
    caregivers,
    "Medical",
    rejected_caregiver
)

if result:
    print("Original Caregiver:", rejected_caregiver)
    print("Rejected the request")
    print()
    print("New Recommended Caregiver:", result["id"])
    print("ETA:", result["eta"], "minutes")
    print("Reason:")
    
    print("Available")
    print("Medical skill matched")
    print("Automatically reassigned")
else:
    print("No alternative caregiver available")