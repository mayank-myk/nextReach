from pydantic import BaseModel


class InfluencerCollabCharge(BaseModel):
    min: str
    avg: str
    max: str
