from typing import Optional

from sqlalchemy.orm import Session

from app.database.influencer_metric_table import InfluencerMetric
from app.database.influencer_table import Influencer
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.requests.influencer_metrics_request import InfluencerMetricRequest
from app.requests.influencer_request import InfluencerRequest
from app.utils.logger import configure_logger

_log = configure_logger()


class InfluencerRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_influencer(self, influencer_id: str, influencer_request: InfluencerRequest) -> Influencer:
        db_influencer = Influencer(
            id=influencer_id,
            created_by=influencer_request.created_by,
            last_updated_by=influencer_request.created_by,
            primary_platform=influencer_request.primary_platform,
            name=influencer_request.name,
            gender=influencer_request.gender,
            phone_number=influencer_request.phone_number,
            email=influencer_request.email,
            address=influencer_request.address,
            profile_picture=influencer_request.profile_picture,
            languages=influencer_request.languages,
            next_reach_score=influencer_request.next_reach_score,
            insta_username=influencer_request.insta_username,
            insta_profile_link=influencer_request.insta_profile_link,
            youtube_username=influencer_request.youtube_username,
            youtube_profile_link=influencer_request.youtube_profile_link,
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

    def update_influencer(self, influencer_id: str, influencer_request: InfluencerRequest) -> Optional[Influencer]:
        try:
            existing_influencer = self.db.query(Influencer).filter(Influencer.id == influencer_id).first()

            if not existing_influencer:
                return None

            db_influencer = Influencer(
                id=existing_influencer.id,
                created_by=existing_influencer.created_by,
                last_updated_by=influencer_request.created_by,
                primary_platform=influencer_request.primary_platform,
                name=influencer_request.name,
                gender=influencer_request.gender,
                phone_number=influencer_request.phone_number,
                email=influencer_request.email,
                address=influencer_request.address,
                profile_picture=influencer_request.profile_picture,
                languages=influencer_request.languages,
                next_reach_score=influencer_request.next_reach_score,
                insta_username=influencer_request.insta_username,
                insta_profile_link=influencer_request.insta_profile_link,
                youtube_username=influencer_request.youtube_username,
                youtube_profile_link=influencer_request.youtube_profile_link,
                fb_username=influencer_request.fb_username,
                fb_profile_link=influencer_request.fb_profile_link,
                niche=influencer_request.niche,
                city=influencer_request.city,
                collab_type=influencer_request.collab_type,
                deliverables=influencer_request.deliverables,
                content_charge=influencer_request.content_charge,
                views_charge=influencer_request.views_charge
            )

            self.db.commit()
            self.db.refresh(db_influencer)
            return db_influencer
        except Exception as ex:
            _log.error("Unable to update influencer record with id {}".format(influencer_id))
            raise FetchOneUserMetadataException(ex, influencer_id)

    def get_influencer_by_id(self, influencer_id: str) -> Optional[Influencer]:

        try:
            existing_influencer = self.db.get(Influencer, influencer_id)

            if not existing_influencer:
                return None

            return existing_influencer

        except Exception as ex:
            _log.error("Unable to fetch influencer for influencer_id {}".format(influencer_id))
            raise FetchOneUserMetadataException(ex, influencer_id)

    def create_influencer_metric(self, influencer_metric_id: str,
                                 influencer_metric_request: InfluencerMetricRequest) -> InfluencerMetric:

        db_influencer_metric = InfluencerMetric(
            id=influencer_metric_id,
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
            insta_spread=influencer_metric_request.insta_spread,
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
            yt_spread=influencer_metric_request.yt_spread,
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
            fb_spread=influencer_metric_request.fb_spread,
            fb_avg_likes=influencer_metric_request.fb_avg_likes,
            fb_avg_comments=influencer_metric_request.fb_avg_comments,
            fb_avg_shares=influencer_metric_request.fb_avg_shares,
            fb_engagement_rate=influencer_metric_request.fb_engagement_rate,
        )

        self.db.add(db_influencer_metric)
        self.db.commit()
        self.db.refresh(db_influencer_metric)
        return db_influencer_metric

    def update_influencer_metric(self, influencer_metric_id: str,
                                 influencer_metric_request: InfluencerMetricRequest) -> InfluencerMetric:
        try:
            existing_influencer_metric = self.db.query(InfluencerMetric).filter(
                InfluencerMetric.id == influencer_metric_id).first()

            if not existing_influencer_metric:
                _log.info("No record found for influencer_metric with id {}".format(influencer_metric_id))
                return None

            db_influencer_metric = InfluencerMetric(
                id=existing_influencer_metric.id,
                created_by=existing_influencer_metric.created_by,
                last_updated_by=influencer_metric_request.created_by,
                influencer_id=existing_influencer_metric.influencer_id,
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
                insta_spread=influencer_metric_request.insta_spread,
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
                yt_spread=influencer_metric_request.yt_spread,
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
                fb_spread=influencer_metric_request.fb_spread,
                fb_avg_likes=influencer_metric_request.fb_avg_likes,
                fb_avg_comments=influencer_metric_request.fb_avg_comments,
                fb_avg_shares=influencer_metric_request.fb_avg_shares,
                fb_engagement_rate=influencer_metric_request.fb_engagement_rate,
            )

            self.db.commit()
            self.db.refresh(db_influencer_metric)
            return db_influencer_metric
        except Exception as ex:
            _log.error("Unable to update influencer_metric record with id {}".format(influencer_metric_id))
            raise FetchOneUserMetadataException(ex, influencer_metric_id)
