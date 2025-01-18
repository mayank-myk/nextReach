from pydantic import BaseModel


class CityDistributionGraph(BaseModel):
    city_1: str
    city_pc_1: int = 0
    city_2: str
    city_pc_2: int = 0
    city_3: str
    city_pc_3: int = 0
