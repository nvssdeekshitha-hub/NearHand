def find_caregiver(caregivers, request_type):

    suitable = []

    for caregiver in caregivers:

        if caregiver["availability"] == "Available" and \
           caregiver["skill"] == request_type:

            suitable.append(caregiver)

    if not suitable:
        return None

    best = min(suitable, key=lambda x: x["eta"])

    return best



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
        "availability": "Busy",
        "skill": "Medical",
        "eta": 5
    }
]


request_type = "Medical"

result = find_caregiver(caregivers, request_type)

if result:
    print("Recommended Caregiver:", result["id"])
    print("ETA:", result["eta"], "minutes")
    print("Reason:")
    print("Available")
    print("Medical skill matched")
    print("Fastest response time")
else:
    print("No suitable caregiver available")