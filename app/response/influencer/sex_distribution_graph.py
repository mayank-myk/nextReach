from pydantic import BaseModel


class SexDistributionGraph(BaseModel):
    men_follower_pc: int = 0
    women_follower_pc: int = 0
