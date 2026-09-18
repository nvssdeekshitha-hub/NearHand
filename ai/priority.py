def get_priority(request_type, urgency):
    if request_type == "Emergency" or urgency == "High":
        return "HIGH"
    elif urgency == "Medium":
        return "MEDIUM"
    else:
        return "LOW"


print(get_priority("Emergency", "High"))