from app.enums.campaign_stage import CampaignStage
from app.enums.status import Status


def campaign_stage_to_status(stage: CampaignStage) -> Status:
    if stage == CampaignStage.CREATED:
        return Status.PROCESSING
    elif stage == CampaignStage.INFLUENCER_FINALIZATION:
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


def int_to_str_k(count: int) -> str:
    if count >= 1000:
        return f"{count // 1000}k"  # Converts to "k" for thousands
    return str(count)  # For values less than 1000, just return the number as a string
