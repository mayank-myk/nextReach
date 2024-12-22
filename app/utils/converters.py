from app.models.campaign_stage import CampaignStage
from app.models.status import Status


def campaign_stage_to_status(stage: CampaignStage) -> Status:
    if stage == CampaignStage.INFLUENCER_FINALIZATION:
        return Status.PROCESSING
    elif stage == CampaignStage.SHOOT:
        return Status.IN_PROGRESS
    elif stage == CampaignStage.POST:
        return Status.IN_PROGRESS
    elif stage == CampaignStage.FIRST_BILLING:
        return Status.IN_PROGRESS
    elif stage == CampaignStage.SECOND_BILLING:
        return Status.IN_PROGRESS
    elif stage == CampaignStage.COMPLETED:
        return Status.COMPLETED
    else:
        return Status.CANCELLED
