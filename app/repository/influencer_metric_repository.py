from typing import Optional, List

from sqlalchemy import func, asc
from sqlalchemy.orm import Session

from app.api_requests.influencer_fb_metric_request import InfluencerFbMetricRequest
from app.api_requests.influencer_insta_metric_request import InfluencerInstaMetricRequest
from app.api_requests.influencer_yt_metric_request import InfluencerYtMetricRequest
from app.api_requests.update_influencer_fb_metric_request import UpdateInfluencerFbMetricRequest
from app.api_requests.update_influencer_insta_metric_request import UpdateInfluencerInstaMetricRequest
from app.api_requests.update_influencer_yt_metric_request import UpdateInfluencerYtMetricRequest
from app.database.influencer_fb_metric_table import InfluencerFbMetric
from app.database.influencer_insta_metric_table import InfluencerInstaMetric
from app.database.influencer_table import Influencer
from app.database.influencer_yt_metric_table import InfluencerYtMetric
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


class InfluencerMetricRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_influencer_insta_metric(self, influencer_id: int,
                                       influencer_metric_request: InfluencerInstaMetricRequest) -> InfluencerInstaMetric:

        db_influencer_metric = InfluencerInstaMetric(
            influencer_id=influencer_id,
            created_by=influencer_metric_request.created_by,
            last_updated_by=influencer_metric_request.created_by,
            username=influencer_metric_request.username,
            profile_link=influencer_metric_request.profile_link,
            followers=influencer_metric_request.followers,
            avg_views=influencer_metric_request.avg_views,
            max_views=influencer_metric_request.max_views,
            consistency_score=influencer_metric_request.consistency_score,
            avg_likes=influencer_metric_request.avg_likes,
            avg_comments=influencer_metric_request.avg_comments,
            avg_shares=influencer_metric_request.avg_shares,
            engagement_rate=influencer_metric_request.engagement_rate,
            city_1=influencer_metric_request.city_1,
            city_pc_1=influencer_metric_request.city_pc_1,
            city_2=influencer_metric_request.city_2,
            city_pc_2=influencer_metric_request.city_pc_2,
            city_3=influencer_metric_request.city_3,
            city_pc_3=influencer_metric_request.city_pc_3,
            age_13_to_17=influencer_metric_request.age_13_to_17,
            age_18_to_24=influencer_metric_request.age_18_to_24,
            age_25_to_34=influencer_metric_request.age_25_to_34,
            age_35_to_44=influencer_metric_request.age_35_to_44,
            age_45_to_54=influencer_metric_request.age_45_to_54,
            age_55=influencer_metric_request.age_55,
            men_follower_pc=influencer_metric_request.men_follower_pc,
            women_follower_pc=influencer_metric_request.women_follower_pc
        )

        self.db.add(db_influencer_metric)
        self.db.commit()
        self.db.refresh(db_influencer_metric)
        return db_influencer_metric

    def create_influencer_yt_metric(self, influencer_id: int,
                                    influencer_metric_request: InfluencerYtMetricRequest) -> InfluencerYtMetric:

        db_influencer_metric = InfluencerYtMetric(
            influencer_id=influencer_id,
            created_by=influencer_metric_request.created_by,
            last_updated_by=influencer_metric_request.created_by,
            username=influencer_metric_request.username,
            profile_link=influencer_metric_request.profile_link,
            followers=influencer_metric_request.followers,
            avg_views=influencer_metric_request.avg_views,
            max_views=influencer_metric_request.max_views,
            consistency_score=influencer_metric_request.consistency_score,
            avg_likes=influencer_metric_request.avg_likes,
            avg_comments=influencer_metric_request.avg_comments,
            avg_shares=influencer_metric_request.avg_shares,
            engagement_rate=influencer_metric_request.engagement_rate,
            city_1=influencer_metric_request.city_1,
            city_pc_1=influencer_metric_request.city_pc_1,
            city_2=influencer_metric_request.city_2,
            city_pc_2=influencer_metric_request.city_pc_2,
            city_3=influencer_metric_request.city_3,
            city_pc_3=influencer_metric_request.city_pc_3,
            age_13_to_17=influencer_metric_request.age_13_to_17,
            age_18_to_24=influencer_metric_request.age_18_to_24,
            age_25_to_34=influencer_metric_request.age_25_to_34,
            age_35_to_44=influencer_metric_request.age_35_to_44,
            age_45_to_54=influencer_metric_request.age_45_to_54,
            age_55=influencer_metric_request.age_55,
            men_follower_pc=influencer_metric_request.men_follower_pc,
            women_follower_pc=influencer_metric_request.women_follower_pc
        )

        self.db.add(db_influencer_metric)
        self.db.commit()
        self.db.refresh(db_influencer_metric)
        return db_influencer_metric

    def create_influencer_fb_metric(self, influencer_id: int,
                                    influencer_metric_request: InfluencerFbMetricRequest) -> InfluencerFbMetric:

        db_influencer_metric = InfluencerFbMetric(
            influencer_id=influencer_id,
            created_by=influencer_metric_request.created_by,
            last_updated_by=influencer_metric_request.created_by,
            username=influencer_metric_request.username,
            profile_link=influencer_metric_request.profile_link,
            followers=influencer_metric_request.followers,
            avg_views=influencer_metric_request.avg_views,
            max_views=influencer_metric_request.max_views,
            consistency_score=influencer_metric_request.consistency_score,
            avg_likes=influencer_metric_request.avg_likes,
            avg_comments=influencer_metric_request.avg_comments,
            avg_shares=influencer_metric_request.avg_shares,
            engagement_rate=influencer_metric_request.engagement_rate,
            city_1=influencer_metric_request.city_1,
            city_pc_1=influencer_metric_request.city_pc_1,
            city_2=influencer_metric_request.city_2,
            city_pc_2=influencer_metric_request.city_pc_2,
            city_3=influencer_metric_request.city_3,
            city_pc_3=influencer_metric_request.city_pc_3,
            age_13_to_17=influencer_metric_request.age_13_to_17,
            age_18_to_24=influencer_metric_request.age_18_to_24,
            age_25_to_34=influencer_metric_request.age_25_to_34,
            age_35_to_44=influencer_metric_request.age_35_to_44,
            age_45_to_54=influencer_metric_request.age_45_to_54,
            age_55=influencer_metric_request.age_55,
            men_follower_pc=influencer_metric_request.men_follower_pc,
            women_follower_pc=influencer_metric_request.women_follower_pc
        )

        self.db.add(db_influencer_metric)
        self.db.commit()
        self.db.refresh(db_influencer_metric)
        return db_influencer_metric

    def update_influencer_insta_metric(self, influencer_insta_metric_id: int,
                                       influencer_metric_request: UpdateInfluencerInstaMetricRequest) -> Optional[
        InfluencerInstaMetric]:
        try:
            existing_influencer_metric = self.db.query(InfluencerInstaMetric).filter(
                InfluencerInstaMetric.id == influencer_insta_metric_id).first()

            if not existing_influencer_metric:
                return None

            setattr(existing_influencer_metric, 'last_updated_by', influencer_metric_request.updated_by)

            if hasattr(influencer_metric_request,
                       'username') and influencer_metric_request.username is not None:
                setattr(existing_influencer_metric, 'username', influencer_metric_request.username)

            if hasattr(influencer_metric_request,
                       'profile_link') and influencer_metric_request.profile_link is not None:
                setattr(existing_influencer_metric, 'profile_link', influencer_metric_request.profile_link)

            if hasattr(influencer_metric_request,
                       'followers') and influencer_metric_request.followers is not None:
                setattr(existing_influencer_metric, 'followers', influencer_metric_request.followers)

            if hasattr(influencer_metric_request,
                       'avg_views') and influencer_metric_request.avg_views is not None:
                setattr(existing_influencer_metric, 'avg_views', influencer_metric_request.avg_views)

            if hasattr(influencer_metric_request,
                       'max_views') and influencer_metric_request.max_views is not None:
                setattr(existing_influencer_metric, 'max_views', influencer_metric_request.max_views)

            if hasattr(influencer_metric_request,
                       'min_views') and influencer_metric_request.min_views is not None:
                setattr(existing_influencer_metric, 'min_views', influencer_metric_request.min_views)

            if hasattr(influencer_metric_request,
                       'consistency_score') and influencer_metric_request.consistency_score is not None:
                setattr(existing_influencer_metric, 'consistency_score',
                        influencer_metric_request.consistency_score)

            if hasattr(influencer_metric_request,
                       'avg_likes') and influencer_metric_request.avg_likes is not None:
                setattr(existing_influencer_metric, 'avg_likes', influencer_metric_request.avg_likes)

            if hasattr(influencer_metric_request,
                       'avg_comments') and influencer_metric_request.avg_comments is not None:
                setattr(existing_influencer_metric, 'avg_comments',
                        influencer_metric_request.avg_comments)

            if hasattr(influencer_metric_request,
                       'avg_shares') and influencer_metric_request.avg_shares is not None:
                setattr(existing_influencer_metric, 'avg_shares',
                        influencer_metric_request.avg_shares)

            if hasattr(influencer_metric_request,
                       'engagement_rate') and influencer_metric_request.engagement_rate is not None:
                setattr(existing_influencer_metric, 'engagement_rate',
                        influencer_metric_request.engagement_rate)

            if hasattr(influencer_metric_request,
                       'city_1') and influencer_metric_request.city_1 is not None:
                setattr(existing_influencer_metric, 'city_1', influencer_metric_request.city_1)

            if hasattr(influencer_metric_request,
                       'city_pc_1') and influencer_metric_request.city_pc_1 is not None:
                setattr(existing_influencer_metric, 'city_pc_1', influencer_metric_request.city_pc_1)

            if hasattr(influencer_metric_request,
                       'city_2') and influencer_metric_request.city_2 is not None:
                setattr(existing_influencer_metric, 'city_2', influencer_metric_request.city_2)

            if hasattr(influencer_metric_request,
                       'city_pc_2') and influencer_metric_request.city_pc_2 is not None:
                setattr(existing_influencer_metric, 'city_pc_2', influencer_metric_request.city_pc_2)

            if hasattr(influencer_metric_request,
                       'city_3') and influencer_metric_request.city_3 is not None:
                setattr(existing_influencer_metric, 'city_3', influencer_metric_request.city_3)

            if hasattr(influencer_metric_request,
                       'city_pc_3') and influencer_metric_request.city_pc_3 is not None:
                setattr(existing_influencer_metric, 'city_pc_3', influencer_metric_request.city_pc_3)

            if hasattr(influencer_metric_request,
                       'age_13_to_17') and influencer_metric_request.age_13_to_17 is not None:
                setattr(existing_influencer_metric, 'age_13_to_17',
                        influencer_metric_request.age_13_to_17)

            if hasattr(influencer_metric_request,
                       'age_18_to_24') and influencer_metric_request.age_18_to_24 is not None:
                setattr(existing_influencer_metric, 'age_18_to_24',
                        influencer_metric_request.age_18_to_24)

            if hasattr(influencer_metric_request,
                       'age_25_to_34') and influencer_metric_request.age_25_to_34 is not None:
                setattr(existing_influencer_metric, 'age_25_to_34',
                        influencer_metric_request.age_25_to_34)

            if hasattr(influencer_metric_request,
                       'age_35_to_44') and influencer_metric_request.age_35_to_44 is not None:
                setattr(existing_influencer_metric, 'age_35_to_44',
                        influencer_metric_request.age_35_to_44)

            if hasattr(influencer_metric_request,
                       'age_45_to_54') and influencer_metric_request.age_45_to_54 is not None:
                setattr(existing_influencer_metric, 'age_45_to_54',
                        influencer_metric_request.age_45_to_54)

            if hasattr(influencer_metric_request,
                       'age_55') and influencer_metric_request.age_55 is not None:
                setattr(existing_influencer_metric, 'age_55', influencer_metric_request.age_55)

            if hasattr(influencer_metric_request,
                       'men_follower_pc') and influencer_metric_request.men_follower_pc is not None:
                setattr(existing_influencer_metric, 'men_follower_pc',
                        influencer_metric_request.men_follower_pc)

            if hasattr(influencer_metric_request,
                       'women_follower_pc') and influencer_metric_request.women_follower_pc is not None:
                setattr(existing_influencer_metric, 'women_follower_pc',
                        influencer_metric_request.women_follower_pc)

            self.db.commit()
            self.db.refresh(existing_influencer_metric)
            return existing_influencer_metric
        except Exception as ex:
            _log.error(
                f"Unable to update influencer_insta_metric record with id {influencer_insta_metric_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(influencer_insta_metric_id))

    def update_influencer_yt_metric(self, influencer_yt_metric_id: int,
                                    influencer_metric_request: UpdateInfluencerYtMetricRequest) -> Optional[
        InfluencerYtMetric]:
        try:
            existing_influencer_metric = self.db.query(InfluencerYtMetric).filter(
                InfluencerYtMetric.id == influencer_yt_metric_id).first()

            if not existing_influencer_metric:
                return None

            setattr(existing_influencer_metric, 'last_updated_by', influencer_metric_request.updated_by)

            if hasattr(influencer_metric_request,
                       'username') and influencer_metric_request.username is not None:
                setattr(existing_influencer_metric, 'username', influencer_metric_request.username)

            if hasattr(influencer_metric_request,
                       'profile_link') and influencer_metric_request.profile_link is not None:
                setattr(existing_influencer_metric, 'profile_link', influencer_metric_request.profile_link)

            if hasattr(influencer_metric_request,
                       'followers') and influencer_metric_request.followers is not None:
                setattr(existing_influencer_metric, 'followers', influencer_metric_request.followers)

            if hasattr(influencer_metric_request,
                       'avg_views') and influencer_metric_request.avg_views is not None:
                setattr(existing_influencer_metric, 'avg_views', influencer_metric_request.avg_views)

            if hasattr(influencer_metric_request,
                       'max_views') and influencer_metric_request.max_views is not None:
                setattr(existing_influencer_metric, 'max_views', influencer_metric_request.max_views)

            if hasattr(influencer_metric_request,
                       'min_views') and influencer_metric_request.min_views is not None:
                setattr(existing_influencer_metric, 'min_views', influencer_metric_request.min_views)

            if hasattr(influencer_metric_request,
                       'consistency_score') and influencer_metric_request.consistency_score is not None:
                setattr(existing_influencer_metric, 'consistency_score',
                        influencer_metric_request.consistency_score)

            if hasattr(influencer_metric_request,
                       'avg_likes') and influencer_metric_request.avg_likes is not None:
                setattr(existing_influencer_metric, 'avg_likes', influencer_metric_request.avg_likes)

            if hasattr(influencer_metric_request,
                       'avg_comments') and influencer_metric_request.avg_comments is not None:
                setattr(existing_influencer_metric, 'avg_comments',
                        influencer_metric_request.avg_comments)

            if hasattr(influencer_metric_request,
                       'avg_shares') and influencer_metric_request.avg_shares is not None:
                setattr(existing_influencer_metric, 'avg_shares',
                        influencer_metric_request.avg_shares)

            if hasattr(influencer_metric_request,
                       'engagement_rate') and influencer_metric_request.engagement_rate is not None:
                setattr(existing_influencer_metric, 'engagement_rate',
                        influencer_metric_request.engagement_rate)

            if hasattr(influencer_metric_request,
                       'city_1') and influencer_metric_request.city_1 is not None:
                setattr(existing_influencer_metric, 'city_1', influencer_metric_request.city_1)

            if hasattr(influencer_metric_request,
                       'city_pc_1') and influencer_metric_request.city_pc_1 is not None:
                setattr(existing_influencer_metric, 'city_pc_1', influencer_metric_request.city_pc_1)

            if hasattr(influencer_metric_request,
                       'city_2') and influencer_metric_request.city_2 is not None:
                setattr(existing_influencer_metric, 'city_2', influencer_metric_request.city_2)

            if hasattr(influencer_metric_request,
                       'city_pc_2') and influencer_metric_request.city_pc_2 is not None:
                setattr(existing_influencer_metric, 'city_pc_2', influencer_metric_request.city_pc_2)

            if hasattr(influencer_metric_request,
                       'city_3') and influencer_metric_request.city_3 is not None:
                setattr(existing_influencer_metric, 'city_3', influencer_metric_request.city_3)

            if hasattr(influencer_metric_request,
                       'city_pc_3') and influencer_metric_request.city_pc_3 is not None:
                setattr(existing_influencer_metric, 'city_pc_3', influencer_metric_request.city_pc_3)

            if hasattr(influencer_metric_request,
                       'age_13_to_17') and influencer_metric_request.age_13_to_17 is not None:
                setattr(existing_influencer_metric, 'age_13_to_17',
                        influencer_metric_request.age_13_to_17)

            if hasattr(influencer_metric_request,
                       'age_18_to_24') and influencer_metric_request.age_18_to_24 is not None:
                setattr(existing_influencer_metric, 'age_18_to_24',
                        influencer_metric_request.age_18_to_24)

            if hasattr(influencer_metric_request,
                       'age_25_to_34') and influencer_metric_request.age_25_to_34 is not None:
                setattr(existing_influencer_metric, 'age_25_to_34',
                        influencer_metric_request.age_25_to_34)

            if hasattr(influencer_metric_request,
                       'age_35_to_44') and influencer_metric_request.age_35_to_44 is not None:
                setattr(existing_influencer_metric, 'age_35_to_44',
                        influencer_metric_request.age_35_to_44)

            if hasattr(influencer_metric_request,
                       'age_45_to_54') and influencer_metric_request.age_45_to_54 is not None:
                setattr(existing_influencer_metric, 'age_45_to_54',
                        influencer_metric_request.age_45_to_54)

            if hasattr(influencer_metric_request,
                       'age_55') and influencer_metric_request.age_55 is not None:
                setattr(existing_influencer_metric, 'age_55', influencer_metric_request.age_55)

            if hasattr(influencer_metric_request,
                       'men_follower_pc') and influencer_metric_request.men_follower_pc is not None:
                setattr(existing_influencer_metric, 'men_follower_pc',
                        influencer_metric_request.men_follower_pc)

            if hasattr(influencer_metric_request,
                       'women_follower_pc') and influencer_metric_request.women_follower_pc is not None:
                setattr(existing_influencer_metric, 'women_follower_pc',
                        influencer_metric_request.women_follower_pc)

            self.db.commit()
            self.db.refresh(existing_influencer_metric)
            return existing_influencer_metric
        except Exception as ex:
            _log.error(
                f"Unable to update influencer_yt_metric record with id {influencer_yt_metric_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(influencer_yt_metric_id))

    def update_influencer_fb_metric(self, influencer_fb_metric_id: int,
                                    influencer_metric_request: UpdateInfluencerFbMetricRequest) -> Optional[
        InfluencerFbMetric]:
        try:
            existing_influencer_metric = self.db.query(InfluencerFbMetric).filter(
                InfluencerFbMetric.id == influencer_fb_metric_id).first()

            if not existing_influencer_metric:
                return None

            setattr(existing_influencer_metric, 'last_updated_by', influencer_metric_request.updated_by)

            if hasattr(influencer_metric_request,
                       'username') and influencer_metric_request.username is not None:
                setattr(existing_influencer_metric, 'username', influencer_metric_request.username)

            if hasattr(influencer_metric_request,
                       'profile_link') and influencer_metric_request.profile_link is not None:
                setattr(existing_influencer_metric, 'profile_link', influencer_metric_request.profile_link)

            if hasattr(influencer_metric_request,
                       'followers') and influencer_metric_request.followers is not None:
                setattr(existing_influencer_metric, 'followers', influencer_metric_request.followers)

            if hasattr(influencer_metric_request,
                       'avg_views') and influencer_metric_request.avg_views is not None:
                setattr(existing_influencer_metric, 'avg_views', influencer_metric_request.avg_views)

            if hasattr(influencer_metric_request,
                       'max_views') and influencer_metric_request.max_views is not None:
                setattr(existing_influencer_metric, 'max_views', influencer_metric_request.max_views)

            if hasattr(influencer_metric_request,
                       'min_views') and influencer_metric_request.min_views is not None:
                setattr(existing_influencer_metric, 'min_views', influencer_metric_request.min_views)

            if hasattr(influencer_metric_request,
                       'consistency_score') and influencer_metric_request.consistency_score is not None:
                setattr(existing_influencer_metric, 'consistency_score',
                        influencer_metric_request.consistency_score)

            if hasattr(influencer_metric_request,
                       'avg_likes') and influencer_metric_request.avg_likes is not None:
                setattr(existing_influencer_metric, 'avg_likes', influencer_metric_request.avg_likes)

            if hasattr(influencer_metric_request,
                       'avg_comments') and influencer_metric_request.avg_comments is not None:
                setattr(existing_influencer_metric, 'avg_comments',
                        influencer_metric_request.avg_comments)

            if hasattr(influencer_metric_request,
                       'avg_shares') and influencer_metric_request.avg_shares is not None:
                setattr(existing_influencer_metric, 'avg_shares',
                        influencer_metric_request.avg_shares)

            if hasattr(influencer_metric_request,
                       'engagement_rate') and influencer_metric_request.engagement_rate is not None:
                setattr(existing_influencer_metric, 'engagement_rate',
                        influencer_metric_request.engagement_rate)

            if hasattr(influencer_metric_request,
                       'city_1') and influencer_metric_request.city_1 is not None:
                setattr(existing_influencer_metric, 'city_1', influencer_metric_request.city_1)

            if hasattr(influencer_metric_request,
                       'city_pc_1') and influencer_metric_request.city_pc_1 is not None:
                setattr(existing_influencer_metric, 'city_pc_1', influencer_metric_request.city_pc_1)

            if hasattr(influencer_metric_request,
                       'city_2') and influencer_metric_request.city_2 is not None:
                setattr(existing_influencer_metric, 'city_2', influencer_metric_request.city_2)

            if hasattr(influencer_metric_request,
                       'city_pc_2') and influencer_metric_request.city_pc_2 is not None:
                setattr(existing_influencer_metric, 'city_pc_2', influencer_metric_request.city_pc_2)

            if hasattr(influencer_metric_request,
                       'city_3') and influencer_metric_request.city_3 is not None:
                setattr(existing_influencer_metric, 'city_3', influencer_metric_request.city_3)

            if hasattr(influencer_metric_request,
                       'city_pc_3') and influencer_metric_request.city_pc_3 is not None:
                setattr(existing_influencer_metric, 'city_pc_3', influencer_metric_request.city_pc_3)

            if hasattr(influencer_metric_request,
                       'age_13_to_17') and influencer_metric_request.age_13_to_17 is not None:
                setattr(existing_influencer_metric, 'age_13_to_17',
                        influencer_metric_request.age_13_to_17)

            if hasattr(influencer_metric_request,
                       'age_18_to_24') and influencer_metric_request.age_18_to_24 is not None:
                setattr(existing_influencer_metric, 'age_18_to_24',
                        influencer_metric_request.age_18_to_24)

            if hasattr(influencer_metric_request,
                       'age_25_to_34') and influencer_metric_request.age_25_to_34 is not None:
                setattr(existing_influencer_metric, 'age_25_to_34',
                        influencer_metric_request.age_25_to_34)

            if hasattr(influencer_metric_request,
                       'age_35_to_44') and influencer_metric_request.age_35_to_44 is not None:
                setattr(existing_influencer_metric, 'age_35_to_44',
                        influencer_metric_request.age_35_to_44)

            if hasattr(influencer_metric_request,
                       'age_45_to_54') and influencer_metric_request.age_45_to_54 is not None:
                setattr(existing_influencer_metric, 'age_45_to_54',
                        influencer_metric_request.age_45_to_54)

            if hasattr(influencer_metric_request,
                       'age_55') and influencer_metric_request.age_55 is not None:
                setattr(existing_influencer_metric, 'age_55', influencer_metric_request.age_55)

            if hasattr(influencer_metric_request,
                       'men_follower_pc') and influencer_metric_request.men_follower_pc is not None:
                setattr(existing_influencer_metric, 'men_follower_pc',
                        influencer_metric_request.men_follower_pc)

            if hasattr(influencer_metric_request,
                       'women_follower_pc') and influencer_metric_request.women_follower_pc is not None:
                setattr(existing_influencer_metric, 'women_follower_pc',
                        influencer_metric_request.women_follower_pc)

            self.db.commit()
            self.db.refresh(existing_influencer_metric)
            return existing_influencer_metric
        except Exception as ex:
            _log.error(
                f"Unable to update influencer_fb_metric record with id {influencer_fb_metric_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(influencer_fb_metric_id))

    def get_latest_influencer_insta_metric(self, influencer_id: int) -> Optional[InfluencerInstaMetric]:
        """
        Fetch the latest metrics for each influencer.
        """
        latest_metric = (
            self.db.query(InfluencerInstaMetric)
            .filter(InfluencerInstaMetric.influencer_id == influencer_id)
            .order_by(InfluencerInstaMetric.id.desc())  # Faster sorting using auto-incremented ID
            .limit(1)
            .one_or_none()
        )
        return latest_metric

    def get_latest_influencer_yt_metric(self, influencer_id: int) -> Optional[InfluencerYtMetric]:
        """
        Fetch the latest metrics for each influencer.
        """
        latest_metric = (
            self.db.query(InfluencerYtMetric)
            .filter(InfluencerYtMetric.influencer_id == influencer_id)
            .order_by(InfluencerYtMetric.id.desc())  # Faster sorting using auto-incremented ID
            .limit(1)
            .one_or_none()
        )
        return latest_metric

    def get_latest_influencer_fb_metric(self, influencer_id: int) -> Optional[InfluencerFbMetric]:
        """
        Fetch the latest Facebook metrics for a given influencer using `id DESC` instead of `created_at DESC`.
        """
        return (
            self.db.query(InfluencerFbMetric)
            .filter(InfluencerFbMetric.influencer_id == influencer_id)
            .order_by(InfluencerFbMetric.id.desc())  # Faster sorting using auto-incremented ID
            .limit(1)
            .one_or_none()
        )

    def get_influencer_data_and_latest_metrics(self, influencer_ids):
        """
        Fetches the latest metrics for influencers across Facebook, YouTube, and Instagram.
        Optimized using `id DESC` instead of `created_at`.
        """

        # 🔹 Subqueries to fetch latest influencer metric IDs using MAX(id)
        latest_fb_metric_subquery = (
            self.db.query(
                InfluencerFbMetric.influencer_id,
                func.max(InfluencerFbMetric.id).label("latest_id")  # Get latest metric ID
            )
            .filter(InfluencerFbMetric.influencer_id.in_(influencer_ids))
            .group_by(InfluencerFbMetric.influencer_id)
            .subquery()
        )

        latest_yt_metric_subquery = (
            self.db.query(
                InfluencerYtMetric.influencer_id,
                func.max(InfluencerYtMetric.id).label("latest_id")  # Get latest metric ID
            )
            .filter(InfluencerYtMetric.influencer_id.in_(influencer_ids))
            .group_by(InfluencerYtMetric.influencer_id)
            .subquery()
        )

        latest_insta_metric_subquery = (
            self.db.query(
                InfluencerInstaMetric.influencer_id,
                func.max(InfluencerInstaMetric.id).label("latest_id")  # Get latest metric ID
            )
            .filter(InfluencerInstaMetric.influencer_id.in_(influencer_ids))
            .group_by(InfluencerInstaMetric.influencer_id)
            .subquery()
        )

        # 🔹 Join each subquery to fetch the latest full metric records
        latest_metrics = (
            self.db.query(
                Influencer.id,
                Influencer.niche,
                Influencer.city,
                Influencer.primary_platform,
                Influencer.profile_picture,
                InfluencerFbMetric.followers.label("fb_followers"),
                InfluencerFbMetric.username.label("fb_username"),
                InfluencerYtMetric.followers.label("yt_followers"),
                InfluencerYtMetric.username.label("yt_username"),
                InfluencerInstaMetric.followers.label("insta_followers"),
                InfluencerInstaMetric.username.label("insta_username")
            )
            .outerjoin(latest_fb_metric_subquery,
                       (latest_fb_metric_subquery.c.influencer_id == Influencer.id))
            .outerjoin(latest_yt_metric_subquery,
                       (latest_yt_metric_subquery.c.influencer_id == Influencer.id))
            .outerjoin(latest_insta_metric_subquery,
                       (latest_insta_metric_subquery.c.influencer_id == Influencer.id))
            .outerjoin(InfluencerFbMetric,
                       (InfluencerFbMetric.id == latest_fb_metric_subquery.c.latest_id))
            .outerjoin(InfluencerYtMetric,
                       (InfluencerYtMetric.id == latest_yt_metric_subquery.c.latest_id))
            .outerjoin(InfluencerInstaMetric,
                       (InfluencerInstaMetric.id == latest_insta_metric_subquery.c.latest_id))
            .filter(Influencer.id.in_(influencer_ids))  # Apply filters as needed
            .all()
        )

        return latest_metrics

    def get_all_influencers_insta_details(self) -> List[InfluencerInstaMetric]:

        return self.db.query(InfluencerInstaMetric).order_by(asc(InfluencerInstaMetric.id)).all()