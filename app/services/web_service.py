import concurrent.futures

import instaloader

from app.api_requests.calculate_earning_request import CalculateEarningRequest
from app.api_requests.waitlist_request import WaitListRequest
from app.repository.wait_list_repository import WaitListRepository
from app.response.enagement_response import EnagementMetric
from app.response.generic_response import GenericResponse
from app.utils.converters import engagement_rate_to_quality, int_to_str_k
from app.utils.logger import configure_logger

_log = configure_logger()


class WebService:
    def __init__(self, session):
        self.wait_list_user_repository = WaitListRepository(session)

    def get_web_metadata(self) -> GenericResponse:
        pass

    def create_lead(self, request: WaitListRequest) -> GenericResponse:
        wait_list = self.wait_list_user_repository.create_wait_list(request=request)

        if wait_list:
            return GenericResponse(success=True,
                                   message="Our team will be in touch with you shortly. Thank you for your patience",
                                   header="Congratulations!", button_text="Continue")
        else:
            return GenericResponse(success=False, message="Something went wrong while create your wait_list",
                                   button_text="Retry")


def calculate_influencer_earning(request: CalculateEarningRequest) -> str:
    view_rate = {
        'FOOD_COOKING': 30,
        'BEAUTY_SKINCARE': 35,
        'TRAVEL_TOURISM': 30,
        'FASHION_LIFESTYLE': 35,
        'HEALTH_FITNESS': 35,
        'TECH_GADGETS': 40,
        'WEALTH_FINANCE': 40,
        'ENTERTAINMENT': 35,
        'GAMING': 40,
        'MOTIVATIONAL_SPIRITUAL': 30,
        'PARENTING_FAMILY': 30,
        'EDUCATION': 35
    }

    content_rate_list = [
        ([0, 10000], 0),
        ([10000, 50000], 5000),
        ([50000, 100000], 10000),
        ([100000, 250000], 15000),
        ([250000, 500000], 20000),
        ([500000, 750000], 25000),
        ([750000, 1000000], 30000),
        ([1000000, 1500000], 35000),
        ([1500000, 2000000], 40000),
        ([2000000, 3000000], 45000),
        ([3000000, 1000000000], 50000)
    ]

    cpm = view_rate.get(request.niche.value, 35)

    # Calculate earnings per post (in INR)
    engagement_multiplier = (request.engagement_rate / 100) + 1  # Adding 1 to base the multiplier
    earnings_per_post = cpm * (request.avg_views / 1000) * engagement_multiplier

    content_price = 50000
    for content_rate in content_rate_list:
        low = content_rate[0][0]
        high = content_rate[0][1]

        if low <= request.follower_count < high:
            content_price = content_rate[1]
            continue

    # Calculate total monthly earnings
    return str(int(content_price + earnings_per_post)) + " per post"


def calculate_engagement_rate1(username: str) -> EnagementMetric | GenericResponse:
    if username == "success":
        return EnagementMetric(
            engagement_rate=3.5,
            engagement_quality=engagement_rate_to_quality(3.5),
            followers=10000,
            likes=1000,
            comments=100
        )
    else:
        return GenericResponse(success=False,
                               message="Please ensure that you have entered a valid public Instagram account username.",
                               button_text="Retry", header="Error")


def calculate_engagement_rate(username: str) -> EnagementMetric | GenericResponse:
    L = instaloader.Instaloader()

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(load_profile_data, L, username)
            result = future.result(timeout=30)
            return result

    except concurrent.futures.TimeoutError:
        return GenericResponse(
            success=False,
            message="The request timed out. Please try again later.",
            button_text="Retry",
            header="Oops"
        )
    except Exception as e:
        return GenericResponse(
            success=False,
            message="We encountered an issue while fetching data from Instagram. Please try again later.",
            button_text="Retry",
            header="Oops"
        )


def load_profile_data(L, username: str) -> EnagementMetric | GenericResponse:
    try:

        profile = instaloader.Profile.from_username(L.context, username)

        # Get the number of followers
        follower_count = profile.followers

        # Initialize total views, likes, and comments
        total_likes = 0
        total_comments = 0
        total_views = 0
        total_posts = 0
        post_count = 0

        # Loop through all posts and collect data
        for post in profile.get_posts():
            total_likes += post.likes
            total_comments += post.comments
            if post.is_video:
                total_views += post.video_view_count  # Video views
            total_posts += 1
            post_count += 1

        if post_count == 0:
            return GenericResponse(success=False,
                                   message="No posts found",
                                   button_text="Understood", header="Oops")

        avg_likes = total_likes / post_count
        avg_comments = total_comments / post_count
        total_engagements = total_likes + total_comments + total_views
        engagement_rate = (total_engagements / (follower_count * post_count))

        return EnagementMetric(
            engagement_rate=f"{engagement_rate:.1f}",
            engagement_quality=engagement_rate_to_quality(engagement_rate),
            followers=int_to_str_k(follower_count),
            likes=int_to_str_k(int(avg_likes)),
            comments=int_to_str_k(int(avg_comments))
        )

    except instaloader.exceptions.ProfileNotExistsException:
        return GenericResponse(success=False,
                               message="Please ensure that you have entered a valid public Instagram account username.",
                               button_text="Retry", header="Error")

    except Exception as e:
        return GenericResponse(
            success=False,
            message="We encountered an issue while fetching data from Instagram. Please try again later.",
            button_text="Retry",
            header="Oops"
        )
