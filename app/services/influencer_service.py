from __future__ import print_function

from datetime import datetime
from io import BytesIO
from typing import Optional, List

import pandas as pd

from app.api_requests.influencer_fb_metric_request import InfluencerFbMetricRequest
from app.api_requests.influencer_insta_metric_request import InfluencerInstaMetricRequest
from app.api_requests.influencer_request import InfluencerRequest
from app.api_requests.influencer_yt_metric_request import InfluencerYtMetricRequest
from app.api_requests.update_influencer_fb_metric_request import UpdateInfluencerFbMetricRequest
from app.api_requests.update_influencer_insta_metric_request import UpdateInfluencerInstaMetricRequest
from app.api_requests.update_influencer_request import UpdateInfluencerRequest
from app.api_requests.update_influencer_yt_metric_request import UpdateInfluencerYtMetricRequest
from app.clients.azure_client import upload_influencer_image
from app.database.influencer_fb_metric_table import InfluencerFbMetric
from app.database.influencer_insta_metric_table import InfluencerInstaMetric
from app.database.influencer_table import Influencer
from app.database.influencer_yt_metric_table import InfluencerYtMetric
from app.repository.influencer_metric_repository import InfluencerMetricRepository
from app.repository.influencer_repository import InfluencerRepository
from app.response.generic_response import GenericResponse
from app.response.influencer_detail_dump import InfluencerDetailDump
from app.utils.logger import configure_logger

_log = configure_logger()


class InfluencerService:
    def __init__(self, session):
        self.influencer_repository = InfluencerRepository(session)
        self.influencer_metric_repository = InfluencerMetricRepository(session)

    def create_influencer(self, request: InfluencerRequest) -> GenericResponse:
        try:
            new_influencer = self.influencer_repository.create_influencer(request)
            return GenericResponse(success=True, header="Success",
                                   message="Influencer created successfully, with influencer_id: {}".format(
                                       new_influencer.id))

        except Exception as e:
            _log.error(
                f"Error occurred while creating new Influencer. Error: {str(e)}")
            return GenericResponse(success=False,
                                   message="Something went wrong while creating new Influencer")

    def upload_image(self, influencer_id: int, image_file) -> GenericResponse:
        try:
            image_url = upload_influencer_image(influencer_id, image_file)
            influencer_found = self.influencer_repository.update_influencer_profile_picture(
                influencer_id=influencer_id,
                profile_picture_path=image_url)
            if influencer_found:
                return GenericResponse(success=True, header="Success",
                                       message="Successfully updated profile picture for influencer having influencer_id: {}".format(
                                           influencer_id))
            else:
                return GenericResponse(success=False,
                                       message="No influencer found for given influencer_id")
        except Exception as e:
            _log.error(
                f"Error occurred while creating new Influencer, influencer_id. Error: {str(e)}")
            return GenericResponse(success=False,
                                   message="Something went wrong while uploading Influencer Image")

    def update_influencer(self, influencer_id: int, request: UpdateInfluencerRequest) -> GenericResponse:
        new_influencer = self.influencer_repository.update_influencer(influencer_id=influencer_id,
                                                                      influencer_request=request)

        if new_influencer:
            return GenericResponse(success=True, header="Success",
                                   message="Successfully updated details for influencer having influencer_id: {}".format(
                                       influencer_id))
        else:
            _log.info("No record found for influencer with id {}".format(influencer_id))
            return GenericResponse(success=False,
                                   message="No influencer found for given influencer_id")

    def create_influencer_insta_metric(self, influencer_id: int,
                                       request: InfluencerInstaMetricRequest) -> GenericResponse:
        try:
            new_influencer_metric = self.influencer_metric_repository.create_influencer_insta_metric(
                influencer_id=influencer_id, influencer_metric_request=request)

            if new_influencer_metric:
                return GenericResponse(success=True, header="Success",
                                       message="Influencer insta metrics created successfully, with influencer_insta_metric_id {}".format(
                                           new_influencer_metric.id))
            else:
                return GenericResponse(success=False,
                                       message="Unable to create new influencer_insta_metric")
        except Exception as e:
            _log.error(
                f"Error occurred while creating new influencer_insta_metric. Error: {str(e)}")
            return GenericResponse(success=False,
                                   message=f"Something went wrong while creating new influencer_insta_metric")

    def create_influencer_yt_metric(self, influencer_id: int, request: InfluencerYtMetricRequest) -> GenericResponse:
        try:
            new_influencer_metric = self.influencer_metric_repository.create_influencer_yt_metric(
                influencer_id=influencer_id, influencer_metric_request=request)

            if new_influencer_metric:
                return GenericResponse(success=True, header="Success",
                                       message="Influencer yt metrics created successfully, with influencer_yt_metric_id {}".format(
                                           new_influencer_metric.id))
            else:
                return GenericResponse(success=False,
                                       message="Unable to create new influencer_yt_metric")
        except Exception as e:
            _log.error(
                f"Error occurred while creating new influencer_yt_metric. Error: {str(e)}")
            return GenericResponse(success=False,
                                   message=f"Something went wrong while creating new influencer_yt_metric")

    def create_influencer_fb_metric(self, influencer_id: int, request: InfluencerFbMetricRequest) -> GenericResponse:
        try:
            new_influencer_metric = self.influencer_metric_repository.create_influencer_fb_metric(
                influencer_id=influencer_id, influencer_metric_request=request)

            if new_influencer_metric:
                return GenericResponse(success=True, header="Success",
                                       message="Influencer fb metrics created successfully, with influencer_fb_metric_id {}".format(
                                           new_influencer_metric.id))
            else:
                return GenericResponse(success=False,
                                       message="Unable to create new influencer_fb_metric")
        except Exception as e:
            _log.error(
                f"Error occurred while creating new influencer_fb_metric. Error: {str(e)}")
            return GenericResponse(success=False,
                                   message=f"Something went wrong while creating new influencer_fb_metric")

    def update_influencer_insta_metric(self, influencer_insta_metric_id: int,
                                       request: UpdateInfluencerInstaMetricRequest) -> GenericResponse:

        new_influencer_metric = self.influencer_metric_repository.update_influencer_insta_metric(
            influencer_insta_metric_id=influencer_insta_metric_id,
            influencer_metric_request=request)

        if new_influencer_metric:
            return GenericResponse(success=True, header="Success",
                                   message="Successfully updated influencer_insta_metrics having influencer_insta_metric_id: {}".format(
                                       influencer_insta_metric_id))
        else:
            _log.info("No record found for influencer_insta_metric with id {}".format(influencer_insta_metric_id))
            return GenericResponse(success=False,
                                   message="No influencer_insta_metric found for given influencer_insta_metric_id")

    def update_influencer_yt_metric(self, influencer_yt_metric_id: int,
                                    request: UpdateInfluencerYtMetricRequest) -> GenericResponse:

        new_influencer_metric = self.influencer_metric_repository.update_influencer_yt_metric(
            influencer_yt_metric_id=influencer_yt_metric_id,
            influencer_metric_request=request)

        if new_influencer_metric:
            return GenericResponse(success=True, header="Success",
                                   message="Successfully updated influencer_yt_metrics having influencer_yt_metric_id: {}".format(
                                       influencer_yt_metric_id))
        else:
            _log.info("No record found for influencer_yt_metric with id {}".format(influencer_yt_metric_id))
            return GenericResponse(success=False,
                                   message="No influencer_yt_metric found for given influencer_yt_metric_id")

    def update_influencer_fb_metric(self, influencer_fb_metric_id: int,
                                    request: UpdateInfluencerFbMetricRequest) -> GenericResponse:

        new_influencer_metric = self.influencer_metric_repository.update_influencer_fb_metric(
            influencer_fb_metric_id=influencer_fb_metric_id,
            influencer_metric_request=request)

        if new_influencer_metric:
            return GenericResponse(success=True, header="Success",
                                   message="Successfully updated influencer_fb_metrics having influencer_fb_metric_id: {}".format(
                                       influencer_fb_metric_id))
        else:
            _log.info("No record found for influencer_fb_metric with id {}".format(influencer_fb_metric_id))
            return GenericResponse(success=False,
                                   message="No influencer_fb_metric found for given influencer_fb_metric_id")

    def get_influencer_detail(self, influencer_id: Optional[int] = None, phone_number: Optional[str] = None,
                              name: Optional[str] = None,
                              insta_username: Optional[str] = None) -> List[Influencer] | GenericResponse:

        influencer = self.influencer_repository.get_influencer_by_attribute(influencer_id=influencer_id,
                                                                            phone_number=phone_number,
                                                                            name=name,
                                                                            insta_username=insta_username)

        if not influencer:
            _log.info("No record found for influencer with id {}".format(influencer_id))
            return GenericResponse(success=False,
                                   message="No influencer found for given influencer_id")

        return influencer

    def get_influencer_insta_metric_detail(self, influencer_id: int) -> InfluencerInstaMetric | GenericResponse:
        influencer_metric = self.influencer_metric_repository.get_latest_influencer_insta_metric(
            influencer_id=influencer_id)

        if not influencer_metric:
            _log.info("No record found for influencer_insta_metric with influencer_id {}".format(influencer_id))
            return GenericResponse(success=False,
                                   message="No influencer_metric found for given influencer_id")

        return influencer_metric

    def get_influencer_yt_metric_detail(self, influencer_id: int) -> InfluencerYtMetric | GenericResponse:
        influencer_metric = self.influencer_metric_repository.get_latest_influencer_yt_metric(
            influencer_id=influencer_id)

        if not influencer_metric:
            _log.info("No record found for influencer_yt_metric with influencer_id {}".format(influencer_id))
            return GenericResponse(success=False,
                                   message="No influencer_metric found for given influencer_id")

        return influencer_metric

    def get_influencer_fb_metric_detail(self, influencer_id: int) -> InfluencerFbMetric | GenericResponse:
        influencer_metric = self.influencer_metric_repository.get_latest_influencer_fb_metric(
            influencer_id=influencer_id)

        if not influencer_metric:
            _log.info("No record found for influencer_fb_metric with influencer_id {}".format(influencer_id))
            return GenericResponse(success=False,
                                   message="No influencer_fb_metric found for given influencer_id")

        return influencer_metric

    def get_all_influencer_detail(self) -> BytesIO:
        try:
            all_influencers = self.influencer_metric_repository.get_influencer_detail_dump()
            influencer_detail_dump_list = []
            for influencer in all_influencers:
                influencer_detail_dump = InfluencerDetailDump(
                    influencer_id=influencer.id,
                    last_updated_at=influencer.last_updated_at.strftime(
                        "%d %b %Y %I:%M %p"),
                    primary_platform=influencer.primary_platform.value,
                    name=influencer.name,
                    phone_number=influencer.phone_number,
                    email=influencer.email,
                    content_charge=influencer.content_charge,
                    views_charge=influencer.views_charge,
                    fixed_charge=influencer.fixed_charge,
                    niche=[niche.value for niche in influencer.niche] if influencer.niche else None,
                    gender=influencer.gender.value if influencer.gender else None,
                    languages=[lang.value for lang in influencer.languages] if influencer.languages else None,
                    next_reach_score=influencer.next_reach_score,
                    blue_tick=influencer.blue_tick,
                    city=influencer.city.value,
                    content_type=influencer.content_type.value,
                    content_subject=influencer.content_subject.value,
                    profile_picture=influencer.profile_picture,
                    collab_type=influencer.collab_type.value,
                    deliverables=influencer.deliverables,
                    influencer_insta_metric_id=influencer.influencer_insta_metric_id,
                    username=influencer.username,
                    profile_link=influencer.profile_link,
                    engagement_rate=influencer.engagement_rate,
                    consistency_score=influencer.consistency_score,
                    followers=influencer.followers,
                    avg_views=influencer.avg_views,
                    max_views=influencer.max_views,
                    avg_likes=influencer.avg_likes,
                    avg_comments=influencer.avg_comments,
                    avg_shares=influencer.avg_shares,
                    city_1=influencer.city_1,
                    city_pc_1=influencer.city_pc_1,
                    city_2=influencer.city_2,
                    city_pc_2=influencer.city_pc_2,
                    city_3=influencer.city_3,
                    city_pc_3=influencer.city_pc_3,
                    age_13_to_17=influencer.age_13_to_17,
                    age_18_to_24=influencer.age_18_to_24,
                    age_25_to_34=influencer.age_25_to_34,
                    age_35_to_44=influencer.age_35_to_44,
                    age_45_to_54=influencer.age_45_to_54,
                    age_55=influencer.age_55,
                    men_follower_pc=influencer.men_follower_pc,
                    women_follower_pc=influencer.women_follower_pc
                )
                influencer_detail_dump_list.append(influencer_detail_dump)

            influencer_data = [influencer.dict() for influencer in influencer_detail_dump_list]

            # Create a DataFrame from the list of dictionaries
            df = pd.DataFrame(influencer_data)

            # Save the DataFrame to a BytesIO buffer
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False,
                            sheet_name=f'Influencer_Details_{datetime.today().strftime("%Y-%m-%d")}')
            buffer.seek(0)
            return buffer

        except Exception as e:
            _log.error(
                f"Error occurred while fetching influencer details dump. Error: {str(e)}")
