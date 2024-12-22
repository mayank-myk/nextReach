from pydantic import BaseModel

from app.response.campaign.billing_info import BillingInfo
from app.response.campaign.campaign_metrics import CampaignMetrics


class CampaignBilling(BaseModel):
    campaign_metrics: CampaignMetrics
    billing_info: BillingInfo
