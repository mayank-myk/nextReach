from __future__ import print_function

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

    def get_influencer_detail(self, influencer_id: int) -> Influencer | GenericResponse:
        influencer = self.influencer_repository.get_influencer_by_id(influencer_id=influencer_id)

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
