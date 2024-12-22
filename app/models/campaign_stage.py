from enum import Enum


class CampaignStage(Enum):
    CREATED = 1
    INFLUENCER_FINALIZATION = 2
    SHOOT = 3
    POST = 4
    FIRST_BILLING = 5
    SECOND_BILLING = 6
    COMPLETED = 7
    CANCELLED = 8
