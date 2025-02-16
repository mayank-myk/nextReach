from datetime import date

from pydantic import BaseModel


class CampaignDraftApprovedRequest(BaseModel):
    content_draft_date: date
