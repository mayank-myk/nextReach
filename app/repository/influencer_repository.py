from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database.influencer_metric_table import InfluencerMetric
from app.database.influencer_table import Influencer
from app.enums.average_view import AverageView
from app.enums.city import City
from app.enums.collab_type import CollabType
from app.enums.content_price import ContentPrice
from app.enums.engagement_rate import EngagementRate
from app.enums.follower_count import FollowerCount
from app.enums.gender import Gender
from app.enums.influencer_age import InfluencerAge
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.enums.rating import Rating
from app.enums.reach_price import ReachPrice
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.api_requests.influencer_metric_request import InfluencerMetricRequest
from app.api_requests.influencer_request import InfluencerRequest
from app.api_requests.update_influencer_metric_request import UpdateInfluencerMetricRequest
from app.api_requests.update_influencer_request import UpdateInfluencerRequest
from app.utils.logger import configure_logger

_log = configure_logger()


class InfluencerRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_influencer(self, influencer_request: InfluencerRequest) -> Influencer:
        db_influencer = Influencer(
            created_by=influencer_request.created_by,
            last_updated_by=influencer_request.created_by,
            primary_platform=influencer_request.primary_platform,
            profile_picture="DEFAULT",
            name=influencer_request.name,
            gender=influencer_request.gender,
            phone_number=influencer_request.phone_number,
            email=influencer_request.email,
            address=influencer_request.address,
            languages=influencer_request.languages,
            next_reach_score=influencer_request.next_reach_score,
            age=influencer_request.age,
            insta_username=influencer_request.insta_username,
            insta_profile_link=influencer_request.insta_profile_link,
            yt_username=influencer_request.yt_username,
            yt_profile_link=influencer_request.yt_profile_link,
            fb_username=influencer_request.fb_username,
            fb_profile_link=influencer_request.fb_profile_link,
            niche=influencer_request.niche,
            city=influencer_request.city,
            collab_type=influencer_request.collab_type,
            deliverables=influencer_request.deliverables,
            content_charge=influencer_request.content_charge,
            views_charge=influencer_request.views_charge
        )

        self.db.add(db_influencer)
        self.db.commit()
        self.db.refresh(db_influencer)
        return db_influencer

    def update_influencer(self, influencer_id: int, influencer_request: UpdateInfluencerRequest) -> Optional[
        Influencer]:
        try:
            existing_influencer = self.db.query(Influencer).filter(Influencer.id == influencer_id).first()

            if not existing_influencer:
                return None

            setattr(existing_influencer, 'last_updated_by', influencer_request.updated_by)

            if hasattr(influencer_request, 'primary_platform') and influencer_request.primary_platform is not None:
                setattr(existing_influencer, 'primary_platform', influencer_request.primary_platform)

            if hasattr(influencer_request, 'name') and influencer_request.name is not None:
                setattr(existing_influencer, 'name', influencer_request.name)

            if hasattr(influencer_request, 'gender') and influencer_request.gender is not None:
                setattr(existing_influencer, 'gender', influencer_request.gender)

            if hasattr(influencer_request, 'phone_number') and influencer_request.phone_number is not None:
                setattr(existing_influencer, 'phone_number', influencer_request.phone_number)

            if hasattr(influencer_request, 'email') and influencer_request.email is not None:
                setattr(existing_influencer, 'email', influencer_request.email)

            if hasattr(influencer_request, 'address') and influencer_request.address is not None:
                setattr(existing_influencer, 'address', influencer_request.address)

            if hasattr(influencer_request, 'languages') and influencer_request.languages is not None:
                setattr(existing_influencer, 'languages', influencer_request.languages)

            if hasattr(influencer_request, 'next_reach_score') and influencer_request.next_reach_score is not None:
                setattr(existing_influencer, 'next_reach_score', influencer_request.next_reach_score)

            if hasattr(influencer_request, 'age') and influencer_request.age is not None:
                setattr(existing_influencer, 'age', influencer_request.age)

            if hasattr(influencer_request, 'insta_username') and influencer_request.insta_username is not None:
                setattr(existing_influencer, 'insta_username', influencer_request.insta_username)

            if hasattr(influencer_request, 'insta_profile_link') and influencer_request.insta_profile_link is not None:
                setattr(existing_influencer, 'insta_profile_link', influencer_request.insta_profile_link)

            if hasattr(influencer_request, 'yt_username') and influencer_request.yt_username is not None:
                setattr(existing_influencer, 'yt_username', influencer_request.yt_username)

            if hasattr(influencer_request, 'yt_profile_link') and influencer_request.yt_profile_link is not None:
                setattr(existing_influencer, 'yt_profile_link', influencer_request.yt_profile_link)

            if hasattr(influencer_request, 'fb_username') and influencer_request.fb_username is not None:
                setattr(existing_influencer, 'fb_username', influencer_request.fb_username)

            if hasattr(influencer_request, 'fb_profile_link') and influencer_request.fb_profile_link is not None:
                setattr(existing_influencer, 'fb_profile_link', influencer_request.fb_profile_link)

            if hasattr(influencer_request, 'niche') and influencer_request.niche is not None:
                setattr(existing_influencer, 'niche', influencer_request.niche)

            if hasattr(influencer_request, 'city') and influencer_request.city is not None:
                setattr(existing_influencer, 'city', influencer_request.city)

            if hasattr(influencer_request, 'collab_type') and influencer_request.collab_type is not None:
                setattr(existing_influencer, 'collab_type', influencer_request.collab_type)

            if hasattr(influencer_request, 'deliverables') and influencer_request.deliverables is not None:
                setattr(existing_influencer, 'deliverables', influencer_request.deliverables)

            if hasattr(influencer_request, 'content_charge') and influencer_request.content_charge is not None:
                setattr(existing_influencer, 'content_charge', influencer_request.content_charge)

            if hasattr(influencer_request, 'views_charge') and influencer_request.views_charge is not None:
                setattr(existing_influencer, 'views_charge', influencer_request.views_charge)

            self.db.commit()
            self.db.refresh(existing_influencer)
            return existing_influencer
        except Exception as ex:
            _log.error(f"Unable to update influencer record with id {influencer_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(influencer_id))

    def update_influencer_profile_picture(self, influencer_id: int, profile_picture_path: str) -> Optional[Influencer]:
        try:
            existing_influencer = self.db.query(Influencer).filter(Influencer.id == influencer_id).first()

            if not existing_influencer:
                return None

            setattr(existing_influencer, 'profile_picture', profile_picture_path)

            self.db.commit()
            self.db.refresh(existing_influencer)
            return existing_influencer
        except Exception as ex:
            _log.error(f"Unable to update influencer record with id {influencer_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(influencer_id))

    def get_influencer_by_id(self, influencer_id: int) -> Optional[Influencer]:

        try:
            existing_influencer = self.db.get(Influencer, influencer_id)

            if not existing_influencer:
                return None

            return existing_influencer

        except Exception as ex:
            _log.error(f"Unable to fetch influencer record with id {influencer_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(influencer_id))

    def create_influencer_metric(self, influencer_metric_request: InfluencerMetricRequest) -> InfluencerMetric:

        db_influencer_metric = InfluencerMetric(
            influencer_id=influencer_metric_request.influencer_id,
            created_by=influencer_metric_request.created_by,
            last_updated_by=influencer_metric_request.created_by,
            insta_followers=influencer_metric_request.insta_followers,
            insta_city_1=influencer_metric_request.insta_city_1,
            insta_city_pc_1=influencer_metric_request.insta_city_pc_1,
            insta_city_2=influencer_metric_request.insta_city_2,
            insta_city_pc_2=influencer_metric_request.insta_city_pc_2,
            insta_city_3=influencer_metric_request.insta_city_3,
            insta_city_pc_3=influencer_metric_request.insta_city_pc_3,
            insta_age_13_to_17=influencer_metric_request.insta_age_13_to_17,
            insta_age_18_to_24=influencer_metric_request.insta_age_18_to_24,
            insta_age_25_to_34=influencer_metric_request.insta_age_25_to_34,
            insta_age_35_to_44=influencer_metric_request.insta_age_35_to_44,
            insta_age_45_to_54=influencer_metric_request.insta_age_45_to_54,
            insta_age_55=influencer_metric_request.insta_age_55,
            insta_men_follower_pc=influencer_metric_request.insta_men_follower_pc,
            insta_women_follower_pc=influencer_metric_request.insta_women_follower_pc,
            insta_avg_views=influencer_metric_request.insta_avg_views,
            insta_max_views=influencer_metric_request.insta_max_views,
            insta_min_views=influencer_metric_request.insta_min_views,
            insta_consistency_score=influencer_metric_request.insta_consistency_score,
            insta_avg_likes=influencer_metric_request.insta_avg_likes,
            insta_avg_comments=influencer_metric_request.insta_avg_comments,
            insta_avg_shares=influencer_metric_request.insta_avg_shares,
            insta_engagement_rate=influencer_metric_request.insta_engagement_rate,
            yt_followers=influencer_metric_request.yt_followers,
            yt_city_1=influencer_metric_request.yt_city_1,
            yt_city_pc_1=influencer_metric_request.yt_city_pc_1,
            yt_city_2=influencer_metric_request.yt_city_2,
            yt_city_pc_2=influencer_metric_request.yt_city_pc_2,
            yt_city_3=influencer_metric_request.yt_city_3,
            yt_city_pc_3=influencer_metric_request.yt_city_pc_3,
            yt_avg_views=influencer_metric_request.yt_avg_views,
            yt_max_views=influencer_metric_request.yt_max_views,
            yt_min_views=influencer_metric_request.yt_min_views,
            yt_consistency_score=influencer_metric_request.yt_consistency_score,
            yt_avg_likes=influencer_metric_request.yt_avg_likes,
            yt_avg_comments=influencer_metric_request.yt_avg_comments,
            yt_avg_shares=influencer_metric_request.yt_avg_shares,
            yt_engagement_rate=influencer_metric_request.yt_engagement_rate,
            fb_followers=influencer_metric_request.fb_followers,
            fb_city_1=influencer_metric_request.fb_city_1,
            fb_city_pc_1=influencer_metric_request.fb_city_pc_1,
            fb_city_2=influencer_metric_request.fb_city_2,
            fb_city_pc_2=influencer_metric_request.fb_city_pc_2,
            fb_city_3=influencer_metric_request.fb_city_3,
            fb_city_pc_3=influencer_metric_request.fb_city_pc_3,
            fb_avg_views=influencer_metric_request.fb_avg_views,
            fb_max_views=influencer_metric_request.fb_max_views,
            fb_min_views=influencer_metric_request.fb_min_views,
            fb_consistency_score=influencer_metric_request.fb_consistency_score,
            fb_avg_likes=influencer_metric_request.fb_avg_likes,
            fb_avg_comments=influencer_metric_request.fb_avg_comments,
            fb_avg_shares=influencer_metric_request.fb_avg_shares,
            fb_engagement_rate=influencer_metric_request.fb_engagement_rate,
        )

        self.db.add(db_influencer_metric)
        self.db.commit()
        self.db.refresh(db_influencer_metric)
        return db_influencer_metric

    def update_influencer_metric(self, influencer_metric_id: int,
                                 influencer_metric_request: UpdateInfluencerMetricRequest) -> Optional[
        InfluencerMetric]:
        try:
            existing_influencer_metric = self.db.query(InfluencerMetric).filter(
                InfluencerMetric.id == influencer_metric_id).first()

            if not existing_influencer_metric:
                return None

            setattr(existing_influencer_metric, 'last_updated_by', influencer_metric_request.updated_by)

            if hasattr(influencer_metric_request,
                       'insta_followers') and influencer_metric_request.insta_followers is not None:
                setattr(existing_influencer_metric, 'insta_followers', influencer_metric_request.insta_followers)

            if hasattr(influencer_metric_request,
                       'insta_city_1') and influencer_metric_request.insta_city_1 is not None:
                setattr(existing_influencer_metric, 'insta_city_1', influencer_metric_request.insta_city_1)

            if hasattr(influencer_metric_request,
                       'insta_city_pc_1') and influencer_metric_request.insta_city_pc_1 is not None:
                setattr(existing_influencer_metric, 'insta_city_pc_1', influencer_metric_request.insta_city_pc_1)

            if hasattr(influencer_metric_request,
                       'insta_city_2') and influencer_metric_request.insta_city_2 is not None:
                setattr(existing_influencer_metric, 'insta_city_2', influencer_metric_request.insta_city_2)

            if hasattr(influencer_metric_request,
                       'insta_city_pc_2') and influencer_metric_request.insta_city_pc_2 is not None:
                setattr(existing_influencer_metric, 'insta_city_pc_2', influencer_metric_request.insta_city_pc_2)

            if hasattr(influencer_metric_request,
                       'insta_city_3') and influencer_metric_request.insta_city_3 is not None:
                setattr(existing_influencer_metric, 'insta_city_3', influencer_metric_request.insta_city_3)

            if hasattr(influencer_metric_request,
                       'insta_city_pc_3') and influencer_metric_request.insta_city_pc_3 is not None:
                setattr(existing_influencer_metric, 'insta_city_pc_3', influencer_metric_request.insta_city_pc_3)

            if hasattr(influencer_metric_request,
                       'insta_age_13_to_17') and influencer_metric_request.insta_age_13_to_17 is not None:
                setattr(existing_influencer_metric, 'insta_age_13_to_17', influencer_metric_request.insta_age_13_to_17)

            if hasattr(influencer_metric_request,
                       'insta_age_18_to_24') and influencer_metric_request.insta_age_18_to_24 is not None:
                setattr(existing_influencer_metric, 'insta_age_18_to_24', influencer_metric_request.insta_age_18_to_24)

            if hasattr(influencer_metric_request,
                       'insta_age_25_to_34') and influencer_metric_request.insta_age_25_to_34 is not None:
                setattr(existing_influencer_metric, 'insta_age_25_to_34', influencer_metric_request.insta_age_25_to_34)

            if hasattr(influencer_metric_request,
                       'insta_age_35_to_44') and influencer_metric_request.insta_age_35_to_44 is not None:
                setattr(existing_influencer_metric, 'insta_age_35_to_44', influencer_metric_request.insta_age_35_to_44)

            if hasattr(influencer_metric_request,
                       'insta_age_45_to_54') and influencer_metric_request.insta_age_45_to_54 is not None:
                setattr(existing_influencer_metric, 'insta_age_45_to_54', influencer_metric_request.insta_age_45_to_54)

            if hasattr(influencer_metric_request,
                       'insta_age_55') and influencer_metric_request.insta_age_55 is not None:
                setattr(existing_influencer_metric, 'insta_age_55', influencer_metric_request.insta_age_55)

            if hasattr(influencer_metric_request,
                       'insta_men_follower_pc') and influencer_metric_request.insta_men_follower_pc is not None:
                setattr(existing_influencer_metric, 'insta_men_follower_pc',
                        influencer_metric_request.insta_men_follower_pc)

            if hasattr(influencer_metric_request,
                       'insta_women_follower_pc') and influencer_metric_request.insta_women_follower_pc is not None:
                setattr(existing_influencer_metric, 'insta_women_follower_pc',
                        influencer_metric_request.insta_women_follower_pc)

            if hasattr(influencer_metric_request,
                       'insta_avg_views') and influencer_metric_request.insta_avg_views is not None:
                setattr(existing_influencer_metric, 'insta_avg_views', influencer_metric_request.insta_avg_views)

            if hasattr(influencer_metric_request,
                       'insta_max_views') and influencer_metric_request.insta_max_views is not None:
                setattr(existing_influencer_metric, 'insta_max_views', influencer_metric_request.insta_max_views)

            if hasattr(influencer_metric_request,
                       'insta_min_views') and influencer_metric_request.insta_min_views is not None:
                setattr(existing_influencer_metric, 'insta_min_views', influencer_metric_request.insta_min_views)

            if hasattr(influencer_metric_request,
                       'insta_consistency_score') and influencer_metric_request.insta_consistency_score is not None:
                setattr(existing_influencer_metric, 'insta_consistency_score',
                        influencer_metric_request.insta_consistency_score)

            if hasattr(influencer_metric_request,
                       'insta_avg_likes') and influencer_metric_request.insta_avg_likes is not None:
                setattr(existing_influencer_metric, 'insta_avg_likes', influencer_metric_request.insta_avg_likes)

            if hasattr(influencer_metric_request,
                       'insta_avg_comments') and influencer_metric_request.insta_avg_comments is not None:
                setattr(existing_influencer_metric, 'insta_avg_comments', influencer_metric_request.insta_avg_comments)

            if hasattr(influencer_metric_request,
                       'insta_avg_shares') and influencer_metric_request.insta_avg_shares is not None:
                setattr(existing_influencer_metric, 'insta_avg_shares', influencer_metric_request.insta_avg_shares)

            if hasattr(influencer_metric_request,
                       'insta_engagement_rate') and influencer_metric_request.insta_engagement_rate is not None:
                setattr(existing_influencer_metric, 'insta_engagement_rate',
                        influencer_metric_request.insta_engagement_rate)

            if hasattr(influencer_metric_request,
                       'yt_followers') and influencer_metric_request.yt_followers is not None:
                setattr(existing_influencer_metric, 'yt_followers', influencer_metric_request.yt_followers)

            if hasattr(influencer_metric_request,
                       'yt_avg_views') and influencer_metric_request.yt_avg_views is not None:
                setattr(existing_influencer_metric, 'yt_avg_views', influencer_metric_request.yt_avg_views)

            if hasattr(influencer_metric_request,
                       'yt_max_views') and influencer_metric_request.yt_max_views is not None:
                setattr(existing_influencer_metric, 'yt_max_views', influencer_metric_request.yt_max_views)

            if hasattr(influencer_metric_request,
                       'yt_min_views') and influencer_metric_request.yt_min_views is not None:
                setattr(existing_influencer_metric, 'yt_min_views', influencer_metric_request.yt_min_views)

            if hasattr(influencer_metric_request,
                       'yt_consistency_score') and influencer_metric_request.yt_consistency_score is not None:
                setattr(existing_influencer_metric, 'yt_consistency_score',
                        influencer_metric_request.yt_consistency_score)

            if hasattr(influencer_metric_request,
                       'yt_avg_likes') and influencer_metric_request.yt_avg_likes is not None:
                setattr(existing_influencer_metric, 'yt_avg_likes', influencer_metric_request.yt_avg_likes)

            if hasattr(influencer_metric_request,
                       'yt_avg_comments') and influencer_metric_request.yt_avg_comments is not None:
                setattr(existing_influencer_metric, 'yt_avg_comments', influencer_metric_request.yt_avg_comments)

            if hasattr(influencer_metric_request,
                       'yt_avg_shares') and influencer_metric_request.yt_avg_shares is not None:
                setattr(existing_influencer_metric, 'yt_avg_shares', influencer_metric_request.yt_avg_shares)

            if hasattr(influencer_metric_request,
                       'yt_engagement_rate') and influencer_metric_request.yt_engagement_rate is not None:
                setattr(existing_influencer_metric, 'yt_engagement_rate',
                        influencer_metric_request.yt_engagement_rate)

            if hasattr(influencer_metric_request, 'yt_city_1') and influencer_metric_request.yt_city_1 is not None:
                setattr(existing_influencer_metric, 'yt_city_1', influencer_metric_request.yt_city_1)

            if hasattr(influencer_metric_request,
                       'yt_city_pc_1') and influencer_metric_request.yt_city_pc_1 is not None:
                setattr(existing_influencer_metric, 'yt_city_pc_1', influencer_metric_request.yt_city_pc_1)

            if hasattr(influencer_metric_request, 'yt_city_2') and influencer_metric_request.yt_city_2 is not None:
                setattr(existing_influencer_metric, 'yt_city_2', influencer_metric_request.yt_city_2)

            if hasattr(influencer_metric_request,
                       'yt_city_pc_2') and influencer_metric_request.yt_city_pc_2 is not None:
                setattr(existing_influencer_metric, 'yt_city_pc_2', influencer_metric_request.yt_city_pc_2)

            if hasattr(influencer_metric_request, 'yt_city_3') and influencer_metric_request.yt_city_3 is not None:
                setattr(existing_influencer_metric, 'yt_city_3', influencer_metric_request.yt_city_3)

            if hasattr(influencer_metric_request,
                       'yt_city_pc_3') and influencer_metric_request.yt_city_pc_3 is not None:
                setattr(existing_influencer_metric, 'yt_city_pc_3', influencer_metric_request.yt_city_pc_3)

            if hasattr(influencer_metric_request,
                       'fb_followers') and influencer_metric_request.fb_followers is not None:
                setattr(existing_influencer_metric, 'fb_followers', influencer_metric_request.fb_followers)

            if hasattr(influencer_metric_request,
                       'fb_avg_views') and influencer_metric_request.fb_avg_views is not None:
                setattr(existing_influencer_metric, 'fb_avg_views', influencer_metric_request.fb_avg_views)

            if hasattr(influencer_metric_request,
                       'fb_max_views') and influencer_metric_request.fb_max_views is not None:
                setattr(existing_influencer_metric, 'fb_max_views', influencer_metric_request.fb_max_views)

            if hasattr(influencer_metric_request,
                       'fb_min_views') and influencer_metric_request.fb_min_views is not None:
                setattr(existing_influencer_metric, 'fb_min_views', influencer_metric_request.fb_min_views)

            if hasattr(influencer_metric_request,
                       'fb_consistency_score') and influencer_metric_request.fb_consistency_score is not None:
                setattr(existing_influencer_metric, 'fb_consistency_score',
                        influencer_metric_request.fb_consistency_score)

            if hasattr(influencer_metric_request,
                       'fb_avg_likes') and influencer_metric_request.fb_avg_likes is not None:
                setattr(existing_influencer_metric, 'fb_avg_likes', influencer_metric_request.fb_avg_likes)

            if hasattr(influencer_metric_request,
                       'fb_avg_comments') and influencer_metric_request.fb_avg_comments is not None:
                setattr(existing_influencer_metric, 'fb_avg_comments', influencer_metric_request.fb_avg_comments)

            if hasattr(influencer_metric_request,
                       'fb_avg_shares') and influencer_metric_request.fb_avg_shares is not None:
                setattr(existing_influencer_metric, 'fb_avg_shares', influencer_metric_request.fb_avg_shares)

            if hasattr(influencer_metric_request,
                       'fb_engagement_rate') and influencer_metric_request.fb_engagement_rate is not None:
                setattr(existing_influencer_metric, 'fb_engagement_rate',
                        influencer_metric_request.fb_engagement_rate)

            if hasattr(influencer_metric_request, 'fb_city_1') and influencer_metric_request.fb_city_1 is not None:
                setattr(existing_influencer_metric, 'fb_city_1', influencer_metric_request.fb_city_1)

            if hasattr(influencer_metric_request,
                       'fb_city_pc_1') and influencer_metric_request.fb_city_pc_1 is not None:
                setattr(existing_influencer_metric, 'fb_city_pc_1', influencer_metric_request.fb_city_pc_1)

            if hasattr(influencer_metric_request, 'fb_city_2') and influencer_metric_request.fb_city_2 is not None:
                setattr(existing_influencer_metric, 'fb_city_2', influencer_metric_request.fb_city_2)

            if hasattr(influencer_metric_request,
                       'fb_city_pc_2') and influencer_metric_request.fb_city_pc_2 is not None:
                setattr(existing_influencer_metric, 'fb_city_pc_2', influencer_metric_request.fb_city_pc_2)

            if hasattr(influencer_metric_request, 'fb_city_3') and influencer_metric_request.fb_city_3 is not None:
                setattr(existing_influencer_metric, 'fb_city_3', influencer_metric_request.fb_city_3)

            if hasattr(influencer_metric_request,
                       'fb_city_pc_3') and influencer_metric_request.fb_city_pc_3 is not None:
                setattr(existing_influencer_metric, 'fb_city_pc_3', influencer_metric_request.fb_city_pc_3)

            self.db.commit()
            self.db.refresh(existing_influencer_metric)
            return existing_influencer_metric
        except Exception as ex:
            _log.error(f"Unable to update influencer_metric record with id {influencer_metric_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(influencer_metric_id))

    def get_latest_influencer_metric(self, influencer_id: int) -> Optional[InfluencerMetric]:
        """
        Fetch the latest metrics for each influencer.
        """
        latest_metric = (
            self.db.query(InfluencerMetric)
            .filter(InfluencerMetric.influencer_id == influencer_id)
            .order_by(InfluencerMetric.created_at.desc())
            .limit(1)
            .one_or_none()
        )
        return latest_metric

    def filter_influencers(
            self,
            page_number: int,
            page_size: int,
            niche: Optional[List[Niche]],
            city: Optional[List[City]],
            reach_price: Optional[List[ReachPrice]],
            follower_count: Optional[List[FollowerCount]],
            avg_views: Optional[List[AverageView]],
            engagement: Optional[EngagementRate],
            platform: Optional[Platform],
            content_price: Optional[ContentPrice],
            collab_type: Optional[CollabType],
            gender: Optional[List[Gender]],
            influencer_age: Optional[List[InfluencerAge]],
            rating: Optional[Rating],
            languages: Optional[List[Language]]
    ):
        """
        Filter influencers based on the criteria.
        """
        # Main Query
        query = (
            self.db.query(Influencer)
            .join(InfluencerMetric, on=(Influencer.id == InfluencerMetric.influencer_id))
            .filter(InfluencerMetric.id.in_(
                self.db.query(InfluencerMetric.id)
                .filter(on=(InfluencerMetric.influencer_id == Influencer.id))
                .order_by(InfluencerMetric.created_at.desc())
                .limit(1)
            )
            )
        )

        # Apply filters
        if niche:
            query = query.filter(Influencer.niche.in_(niche))
        if city:
            query = query.filter(Influencer.city.in_(city))
        if reach_price:
            filters = [
                Influencer.views_charge.between(price.value[0], price.value[1])
                for price in reach_price
            ]
            query = query.filter(or_(*filters))
        if follower_count:
            filters = [
                InfluencerMetric.insta_followers.between(fc.value[0], fc.value[1])
                for fc in follower_count
            ]
            query = query.filter(or_(*filters))
        if avg_views:
            filters = [
                InfluencerMetric.insta_avg_views.between(av.value[0], av.value[1])
                for av in avg_views
            ]
            query = query.filter(or_(*filters))
        if engagement:
            query = query.filter(
                InfluencerMetric.insta_engagement_rate.between(engagement.value[0], engagement.value[1]))
        if platform:
            query = query.filter(Influencer.primary_platform == platform)
        if content_price:
            query = query.filter(Influencer.content_charge.between(content_price.value[0], content_price.value[1]))
        if collab_type:
            query = query.filter(Influencer.collab_type == collab_type)
        if gender:
            query = query.filter(Influencer.gender.in_(gender))
        if influencer_age:
            filters = [
                Influencer.age.between(ia.value[0], ia.value[1])
                for ia in influencer_age
            ]
            query = query.filter(or_(*filters))
        if languages:
            query = query.filter(Influencer.languages.any(Influencer.languages.in_(languages)))

        # Pagination
        influencers = query.limit(page_size).offset((page_number - 1) * page_size).all()
        return influencers
