from pydantic import BaseModel


class InfluencerCollabCharge(BaseModel):
    min: int
    average: int
    max: int
