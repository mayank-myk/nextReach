from pydantic import BaseModel

from app.enums.city import City


class CityDistributionGraph(BaseModel):
    city_1: City
    city_pc_1: int = 0
    city_2: City
    city_pc_2: int = 0
    city_3: City
    city_pc_3: int = 0
