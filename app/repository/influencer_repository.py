from typing import Optional, List

from sqlalchemy import or_, func, desc
from sqlalchemy.orm import Session, aliased

from app.api_requests.influencer_request import InfluencerRequest
from app.api_requests.update_influencer_request import UpdateInfluencerRequest
from app.database.influencer_fb_metric_table import InfluencerFbMetric
from app.database.influencer_insta_metric_table import InfluencerInstaMetric
from app.database.influencer_table import Influencer
from app.database.influencer_yt_metric_table import InfluencerYtMetric
from app.enums.average_view import AverageView, VIEW_DICT
from app.enums.city import City
from app.enums.collab_type import CollabType, COLLAB_TYPE_DICT
from app.enums.content_price import ContentPrice, CONTENT_PRICE_DICT
from app.enums.engagement_rate import EngagementRate, ER_DICT
from app.enums.follower_count import FollowerCount, FOLLOWER_COUNT_DICT
from app.enums.gender import Gender
from app.enums.language import Language
from app.enums.niche import Niche
from app.enums.platform import Platform
from app.enums.rating import Rating
from app.enums.reach_price import ReachPrice, REACH_PRICE_DICT
from app.enums.sort_applied import SortApplied
from app.exceptions.repository_exceptions import FetchOneUserMetadataException
from app.utils.logger import configure_logger

_log = configure_logger()


def get_influencer_metric_table(platform):
    platform_table_map = {
        Platform.INSTAGRAM: InfluencerInstaMetric,
        Platform.YOUTUBE: InfluencerYtMetric,
        Platform.FACEBOOK: InfluencerFbMetric,
    }
    metric_table = platform_table_map.get(platform, InfluencerInstaMetric)  # Default to Instagram if not specified
    return metric_table


class InfluencerRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_influencer(self, influencer_request: InfluencerRequest) -> Influencer:
        db_influencer = Influencer(
            created_by=influencer_request.created_by,
            last_updated_by=influencer_request.created_by,
            primary_platform=influencer_request.primary_platform,
            profile_picture="https://nextreachblob.blob.core.windows.net/profile-picture/default",
            name=influencer_request.name,
            gender=influencer_request.gender,
            phone_number=influencer_request.phone_number,
            email=influencer_request.email,
            address=influencer_request.address,
            languages=influencer_request.languages,
            next_reach_score=influencer_request.next_reach_score,
            dob=influencer_request.dob,
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

            if hasattr(influencer_request, 'dob') and influencer_request.dob is not None:
                setattr(existing_influencer, 'dob', influencer_request.dob)

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

    def get_influencer_by_attribute(self, influencer_id: Optional[int] = None,
                                    phone_number: Optional[str] = None,
                                    name: Optional[str] = None,
                                    insta_username: Optional[str] = None) -> Optional[List[Influencer]]:

        try:
            query = self.db.query(Influencer)

            # Dynamically add filters based on the provided parameters
            if influencer_id:
                query = query.filter(Influencer.id == influencer_id)
            if phone_number:
                query = query.filter(Influencer.phone_number == phone_number)
            if name:
                query = query.filter(Influencer.name.ilike(f"%{name}%"))  # Partial match, case-insensitive
            if insta_username:
                query = query.join(Influencer.influencer_insta_metric).filter(
                    InfluencerInstaMetric.username.ilike(f"%{insta_username}%")
                )

            existing_influencer = query.all()

            if not existing_influencer:
                return None

            return existing_influencer

        except Exception as ex:
            _log.error(f"Unable to fetch influencer record with id {influencer_id}. Error: {str(ex)}")
            raise FetchOneUserMetadataException(ex, str(influencer_id))

    def filter_matched_influencers(
            self,
            page_number: int,
            page_size: int,
            sort_applied: SortApplied,
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
            rating: Optional[Rating],
            language_list: Optional[List[Language]]
    ):

        metric_table = get_influencer_metric_table(platform)
        metric_alias = aliased(metric_table)

        query = (
            self.db.query(Influencer)
            .join(metric_table, Influencer.id == metric_table.influencer_id)
            .filter(metric_table.id.in_(
                self.db.query(metric_alias.id)  # Use the alias here
                .filter(metric_alias.influencer_id == Influencer.id)  # Correlate with the outer query
                .order_by(metric_alias.created_at.desc())
                .limit(1)
            ))
        )

        # Apply filters
        if niche:
            query = query.filter(
                (Influencer.niche.op("&&")(niche)) |  # Overlap operator for non-empty arrays
                (Influencer.niche.is_(None)) |  # Check for None values
                (func.cardinality(Influencer.niche) == 0)  # Check for empty array
            )
        if city:
            query = query.filter(Influencer.city.in_(city))
        if reach_price:
            filters = [
                Influencer.views_charge.between(REACH_PRICE_DICT[price][0], REACH_PRICE_DICT[price][1])
                for price in reach_price
            ]
            query = query.filter(or_(*filters))
        if follower_count:
            filters = [
                metric_table.followers.between(FOLLOWER_COUNT_DICT[fc][0],
                                               FOLLOWER_COUNT_DICT[fc][1])
                for fc in follower_count
            ]
            query = query.filter(or_(*filters))
        if avg_views:
            filters = [
                metric_table.avg_views.between(VIEW_DICT[av][0], VIEW_DICT[av][1])
                for av in avg_views
            ]
            query = query.filter(or_(*filters))
        if engagement:
            query = query.filter(
                metric_table.engagement_rate.between(ER_DICT[engagement][0],
                                                     ER_DICT[engagement][1]))
        if platform:
            query = query.filter(Influencer.primary_platform == platform)
        if content_price:
            query = query.filter(Influencer.content_charge.between(CONTENT_PRICE_DICT[content_price][0],
                                                                   CONTENT_PRICE_DICT[content_price][1]))
        if collab_type:
            query = query.filter(Influencer.collab_type.in_(COLLAB_TYPE_DICT[collab_type]))
        if gender:
            query = query.filter(Influencer.gender.in_(gender))
        if language_list:
            query = query.filter(
                (Influencer.languages.op("&&")(language_list)) |  # Overlap operator for non-empty arrays
                (Influencer.languages.is_(None)) |  # Check for None values
                (func.cardinality(Influencer.languages) == 0)  # Check for empty array
            )

        # Apply sorting based on the 'sort_applied' parameter
        if sort_applied == SortApplied.CONTENT_PRICE_LOW_TO_HIGH:
            query = query.order_by(Influencer.content_charge.asc())  # Sort by content charge in ascending order
        elif sort_applied == SortApplied.CONTENT_PRICE_HIGH_TO_LOW:
            query = query.order_by(Influencer.content_charge.desc())  # Sort by content charge in descending order
        elif sort_applied == SortApplied.VIEWS_CHARGE_LOW_TO_HIGH:
            query = query.order_by(Influencer.views_charge.asc())  # Sort by views charge in ascending order
        elif sort_applied == SortApplied.VIEWS_CHARGE_HIGH_TO_LOW:
            query = query.order_by(Influencer.views_charge.desc())  # Sort by views charge in descending order
        else:
            query = query.order_by(
                desc(Influencer.next_reach_score))  # Sort by next_reach_score in descending order

        # Pagination
        all_matched_influencers = query.all()
        matched_influencers = query.limit(page_size).offset((page_number - 1) * page_size).all()

        return matched_influencers, all_matched_influencers

    def filter_unmatched_influencers(
            self,
            matched_influencers,
            all_matched_influencers,
            page_number: int,
            page_size: int,
            sort_applied: SortApplied,
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
            rating: Optional[Rating],
            language_list: Optional[List[Language]]
    ):

        all_matched_influencer_ids = [matched_influencer.id for matched_influencer in all_matched_influencers]

        metric_table = get_influencer_metric_table(platform)
        metric_alias = aliased(metric_table)
        query = (
            self.db.query(Influencer)
            .join(metric_table, Influencer.id == metric_table.influencer_id)
            .filter(metric_table.id.in_(
                self.db.query(metric_alias.id)  # Use the alias here
                .filter(metric_alias.influencer_id == Influencer.id)  # Correlate with the outer query
                .order_by(metric_alias.created_at.desc())
                .limit(1)
            ))
            .filter(Influencer.id.notin_(all_matched_influencer_ids))
        )

        # Apply filters
        # if niche:
        #     query = query.filter(
        #         (Influencer.niche.op("&&")(niche)) |  # Overlap operator for non-empty arrays
        #         (Influencer.niche.is_(None)) |  # Check for None values
        #         (func.cardinality(Influencer.niche) == 0)  # Check for empty array
        #     )
        # if platform:
        #     query = query.filter(Influencer.primary_platform == platform)
        # if language_list:
        #     query = query.filter(
        #         (Influencer.languages.op("&&")(language_list)) |  # Overlap operator for non-empty arrays
        #         (Influencer.languages.is_(None)) |  # Check for None values
        #         (func.cardinality(Influencer.languages) == 0)  # Check for empty array
        #     )

        # Apply sorting based on the 'sort_applied' parameter
        if sort_applied == SortApplied.CONTENT_PRICE_LOW_TO_HIGH:
            query = query.order_by(Influencer.content_charge.asc())  # Sort by content charge in ascending order
        elif sort_applied == SortApplied.CONTENT_PRICE_HIGH_TO_LOW:
            query = query.order_by(Influencer.content_charge.desc())  # Sort by content charge in descending order
        elif sort_applied == SortApplied.VIEWS_CHARGE_LOW_TO_HIGH:
            query = query.order_by(Influencer.views_charge.asc())  # Sort by views charge in ascending order
        elif sort_applied == SortApplied.VIEWS_CHARGE_HIGH_TO_LOW:
            query = query.order_by(Influencer.views_charge.desc())  # Sort by views charge in descending order
        else:
            query = query.order_by(
                desc(Influencer.next_reach_score))  # Sort by next_reach_score in descending order

        # Pagination
        all_unmatched_influencers = query.all()
        if page_size - len(matched_influencers) < 0:
            unmatched_influencers = []
        else:
            matched_pages = len(all_matched_influencer_ids) // page_size
            remaining_matched = len(all_matched_influencer_ids) % page_size
            offset = max(0, (page_number - matched_pages - 1) * page_size - remaining_matched)
            unmatched_influencers = query.limit(page_size - len(matched_influencers)).offset(offset).all()

        return unmatched_influencers, all_unmatched_influencers

    def get_top_rated_influencers(self) -> List[Influencer]:

        return self.db.query(Influencer).order_by(desc(Influencer.next_reach_score)).limit(30).offset(0).all()
