from fastapi import FastAPI
from pydantic import BaseModel

from ai.priority import get_priority
from ai.matching import find_caregiver

app = FastAPI()


# Request format
class HelpRequest(BaseModel):
    request_type: str
    urgency: str


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
        "skill": "General",
        "eta": 12
    }
]


# AI recommendation API
@app.post("/ai/recommend")
def recommend(data: HelpRequest):

    # Find priority
    priority = get_priority(
        data.request_type,
        data.urgency
    )

    # Find suitable caregiver
    caregiver = find_caregiver(
        caregivers,
        data.request_type
    )

    # If no caregiver is available
    if caregiver is None:
        return {
            "priority": priority,
            "message": "No suitable caregiver available"
        }

    # Return recommendation
    return {
        "priority": priority,
        "caregiver_id": caregiver["id"],
        "eta": caregiver["eta"],
        "reason": [
            "Caregiver is available",
            "Required skill matched",
            "Fast response time"
        ]
    }