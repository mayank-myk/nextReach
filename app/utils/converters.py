from app.enums.campaign_stage import CampaignStage
from app.enums.status import Status


def campaign_stage_to_status(stage: CampaignStage) -> Status:
    if stage == CampaignStage.CREATED:
        return Status.PROCESSING
    elif stage in [CampaignStage.INFLUENCER_FINALIZATION, CampaignStage.SHOOT, CampaignStage.DRAFT, CampaignStage.POST,
                   CampaignStage.FIRST_BILLING, CampaignStage.SECOND_BILLING]:
        return Status.IN_PROGRESS
    elif stage == CampaignStage.COMPLETED:
        return Status.COMPLETED
    else:
        return Status.CANCELLED


def int_to_str_k(count) -> str:
    if count and count >= 10000:
        value = count / 1000
        if value % 1 == 0:  # If the number is an integer
            return f"{int(value)}k"
        else:
            return f"{value:.2f}k"  # Converts to "k" for thousands
    elif count:
        return str(count)  # For values less than 1000, just return the number as a string
    else:
        return ""


def engagement_rate_to_quality(engagement_rate: float) -> str:
    if engagement_rate <= 1.0:
        return "LOW"
    elif 1.0 < engagement_rate <= 3.0:
        return "GOOD"
    elif 3.0 < engagement_rate <= 6.0:
        return "EXCELLENT"
    else:
        return "OUTSTANDING"


def combine_names(name1: str, name2: str) -> str:
    # Replace None values with an empty string
    name1 = name1 if name1 is not None else ""
    name2 = name2 if name2 is not None else ""

    # If both names are empty, return an empty string
    if not name1 and not name2:
        return ""

    # Combine names with a comma, ensuring no trailing or leading commas
    return f"{name1}, {name2}" if name1 and name2 else f"{name1}{name2}"
