import concurrent.futures
import json
import random

import instaloader
import requests

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


def calculate_engagement_rate2(username: str) -> EnagementMetric | GenericResponse:
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


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Galaxy S10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36"
]

# More realistic headers with dynamic and rotating headers
HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),  # Randomly select a User-Agent from the list
    "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.instagram.com/",
    "Accept": "*/*"
    # "x-ig-app-id": "936619743392459",  # Instagram app id (static for all)
    # "x-ig-www-claim": "hmac.4e2d882f1c0ac7d2c6c1de1b318f69b7ff84d052",  # Claim header (static for all)
    # "x-ig-session-id": str(random.randint(100000000, 999999999)),  # Random session ID
    # "x-ig-android-id": str(random.randint(1000000000000000, 9999999999999999)),  # Random Android ID
    # "x-ig-android-serial": str(random.randint(1000000000000000, 9999999999999999)),  # Random Android serial
    # "x-ig-device-id": str(random.randint(1000000000000000, 9999999999999999)),  # Device ID
    # "x-ig-ds-user-id": str(random.randint(1000000000, 9999999999)),  # User ID (randomized)
    # "x-ig-connection-type": "WIFI",  # Simulate WIFI connection
    # "x-ig-batch": "1",  # Batch request type
}


def calculate_engagement_rate(username: str) -> EnagementMetric | GenericResponse:
    L = instaloader.Instaloader()

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(scrap_data_using_official_api, username)
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


def get_instagram_data(username: str):
    # Instagram API URL
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

    # Make the GET request to fetch profile data
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None

    try:
        profile_data = response.json()
    except UnicodeError:
        profile_data = json.loads(response.text)
    except json.JSONDecodeError:
        return None

    return profile_data


def scrap_data_using_official_api(username: str) -> EnagementMetric | GenericResponse:
    profile_data = get_instagram_data(username)

    if not profile_data:
        return GenericResponse(
            success=False,
            message="We encountered an issue while fetching data from Instagram. Please try again later.",
            button_text="Retry",
            header="Oops"
        )

    # Extract the user data from the profile JSON response
    user_data = profile_data.get("data", {}).get("user", {})

    if not user_data:
        return GenericResponse(success=False,
                               message="Please ensure that you have entered a valid public Instagram account username.",
                               button_text="Retry", header="Error")

    # Followers count
    followers_count = user_data.get("edge_followed_by", {}).get("count", 0)

    if followers_count == 0:
        return GenericResponse(
            success=False,
            message="We encountered an issue while fetching data from Instagram. Please try again later.",
            button_text="Retry",
            header="Oops"
        )

    # Get recent posts (You might have to adjust this depending on available post data)
    posts = user_data.get("edge_owner_to_timeline_media", {}).get("edges", [])

    if not posts:
        return GenericResponse(success=False,
                               message="Please ensure that you have entered a valid public Instagram account username.",
                               button_text="Retry", header="Error")

    total_likes = 0
    total_comments = 0
    total_views = 0
    post_count = 0

    # Iterate through recent posts (Let's use the first 12 posts as an example)
    for post in posts[:12]:  # Adjust this to the number of posts you want
        node = post.get("node", {})
        total_likes += node.get("edge_media_preview_like", {}).get("count", 0)
        total_comments += node.get("edge_media_to_comment", {}).get("count", 0)
        total_views += node.get("video_view_count", 0)  # For video posts, get the view count
        post_count += 1

    if post_count == 0:
        return GenericResponse(
            success=False,
            message="We encountered an issue while fetching data from Instagram. Please try again later.",
            button_text="Retry",
            header="Oops"
        )

    # Calculate engagement rate
    total_engagement = total_likes + total_comments + total_views
    engagement_rate = (total_engagement / (followers_count * post_count))

    return EnagementMetric(
        engagement_rate=f"{engagement_rate:.1f}",
        engagement_quality=engagement_rate_to_quality(engagement_rate),
        followers=int_to_str_k(followers_count),
        likes=int_to_str_k(int(total_likes / post_count)),
        comments=int_to_str_k(int(total_comments / post_count))
    )


def calculate_engagement_rate1(username: str) -> EnagementMetric | GenericResponse:
    L = instaloader.Instaloader()

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(load_data_using_instaloader, L, username)
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


def load_data_using_instaloader(L, username: str) -> EnagementMetric | GenericResponse:
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

        avg_likes = total_likes
        avg_comments = total_comments
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
