from pydantic import BaseModel


class InfluencerCollabCharge(BaseModel):
    min: int
    avg: int
    max: int
