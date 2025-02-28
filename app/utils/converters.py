from typing import Optional, List, Dict

from app.enums.campaign_stage import CampaignStage
from app.enums.status import Status


def campaign_stage_to_status(stage: CampaignStage) -> Status:
    if stage == CampaignStage.CREATED:
        return Status.PROCESSING
    elif stage in [CampaignStage.INFLUENCER_FINALIZED, CampaignStage.SHOOT_COMPLETED, CampaignStage.DRAFT_APPROVED,
                   CampaignStage.CONTENT_POSTED,
                   CampaignStage.DAY2_BILLING, CampaignStage.DAY8_BILLING]:
        return Status.IN_PROGRESS
    elif stage == CampaignStage.COMPLETED:
        return Status.COMPLETED
    else:
        return Status.CANCELLED


def int_to_str_k(count) -> Optional[str]:
    if not count or not isinstance(count, (int, float)) or count < 0:
        return None  # Return None for None or 0 values

    if count >= 1000000:  # For millions
        value = round(count / 1000000, 1)
        if value % 1 == 0:  # If the number is an integer
            return f"{int(value)} M"
        else:
            return f"{value} M"  # Converts to "m" for millions

    elif count >= 1000:  # For thousands
        value = round(count / 1000, 1)
        if value % 1 == 0:  # If the number is an integer
            return f"{int(value)}K"
        else:
            return f"{value}K"  # Converts to "k" for thousands

    return str(count)  # For values less than 1,000, return as a string


def float_to_str(value) -> Optional[str]:
    if value is None or value == 0:
        return "0"

    if value.is_integer():
        return str(int(value))

    return f"{round(value, 1):.1f}".rstrip("0").rstrip(".") + "%"


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


def format_to_rupees(value: int):
    if value and value > 0:
        value_str = str(value)[::-1]  # Reverse the string for easier grouping
        formatted = [value_str[:3]]  # First group of 3 digits

        # Process subsequent groups of 2 digits
        for i in range(3, len(value_str), 2):
            formatted.append(value_str[i:i + 2])

        # Combine the reversed groups with commas, then reverse the final string
        return "₹" + ','.join(formatted)[::-1]
    else:
        return None


def format_to_currency(value: int):
    if value and value > 0:
        value_str = str(value)[::-1]  # Reverse the string for easier grouping
        formatted = [value_str[:3]]  # First group of 3 digits

        # Process subsequent groups of 2 digits
        for i in range(3, len(value_str), 2):
            formatted.append(value_str[i:i + 2])

        # Combine the reversed groups with commas, then reverse the final string
        return ','.join(formatted)[::-1]
    else:
        return "NOT_FOUND"


def format_to_views_charge(value: int):
    if value and value > 0:
        return "₹" + str(value) + " per 1000 views"
    else:
        return None


def city_distribution_to_dict(city_1: str, city_pc_1: int, city_2: str, city_pc_2: int, city_3: str, city_pc_3: int) -> \
        Optional[List[Dict[str, int]]]:
    if city_1 and city_2 and city_3 and city_pc_1 and city_pc_2 and city_pc_3:

        return [{"city": city_1, "value": city_pc_1}, {"city": city_2, "value": city_pc_2},
                {"city": city_3, "value": city_pc_3}]
    else:
        return None


def age_distribution_to_dict(age_13_to_17: int, age_18_to_24: int, age_25_to_34: int, age_35_to_44: int,
                             age_45_to_54: int, age_55: int) -> Optional[List[Dict[str, int]]]:
    if age_13_to_17 and age_18_to_24 and age_25_to_34 and age_35_to_44 and age_45_to_54 and age_55:
        return [{"age": "13-17", "value": age_13_to_17}, {"age": "18-24", "value": age_18_to_24},
                {"age": "25-34", "value": age_25_to_34}, {"age": "35-44", "value": age_35_to_44},
                {"age": "45-54", "value": age_45_to_54}, {"age": "55+", "value": age_55}]
    else:
        return None


def sex_distribution_to_dict(men_follower_pc: int, women_follower_pc: int) -> Optional[List[Dict[str, int]]]:
    if men_follower_pc and women_follower_pc:
        return [{"name": "Male", "value": men_follower_pc}, {"name": "Female", "value": women_follower_pc}]
    else:
        return None


def campaign_stage_to_user_friendly_str(campaign_stage: CampaignStage):
    if not campaign_stage:
        return "NOT_FOUND"

    if campaign_stage == CampaignStage.INFLUENCER_FINALIZED:
        return "INFLUENCER-FINALIZED"
    elif campaign_stage == CampaignStage.SHOOT_COMPLETED:
        return "CONTENT-SHOOT-COMPLETED"
    elif campaign_stage == CampaignStage.DRAFT_APPROVED:
        return "CONTENT-DRAFT-APPROVED"
    elif campaign_stage == CampaignStage.CONTENT_POSTED:
        return "CONTENT-POSTED"
    elif campaign_stage == CampaignStage.DAY2_BILLING:
        return "DAY2-PAYMENT-UPDATED"
    elif campaign_stage == CampaignStage.DAY8_BILLING:
        return "DAY8-PAYMENT-UPDATED"
    elif campaign_stage == CampaignStage.COMPLETED:
        return "COMPLETED"
    elif campaign_stage == CampaignStage.CANCELLED:
        return "CANCELLED"
    else:
        return ""
