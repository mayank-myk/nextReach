from pydantic import BaseModel


class AgeDistributionGraph(BaseModel):
    age_13_to_17: int = 0
    age_18_to_24: int = 0
    age_25_to_34: int = 0
    age_35_to_44: int = 0
    age_45_to_54: int = 0
    age_55: int = 0
