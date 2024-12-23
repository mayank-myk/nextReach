from __future__ import print_function

from app.repository.influencer_repository import InfluencerRepository
from app.requests.influencer_metrics_request import InfluencerMetricRequest
from app.requests.influencer_request import InfluencerRequest
from app.response.generic_response import GenericResponse
from app.utils import id_utils
from app.utils.logger import configure_logger

_log = configure_logger()


class InfluencerService:
    def __init__(self, session):
        self.influencer_repository = InfluencerRepository(session)

    def create_influencer(self, request: InfluencerRequest) -> GenericResponse:
        timestamp_id = id_utils.get_influencer_id()
        try:
            new_influencer = self.influencer_repository.create_influencer(timestamp_id, request)

            if new_influencer:
                return GenericResponse(success=True, button_text=None, message=None)
            else:
                return GenericResponse(success=False, button_text=None, message="Unable to create new influencer")
        except Exception as e:
            _log.error(
                f"Error occurred while creating new Influencer, influencer_id: {timestamp_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text=None,
                                   message=f"Something went wrong while creating new Influencer, influencer_id: {timestamp_id}")

    def update_influencer(self, influencer_id: str, request: InfluencerRequest) -> GenericResponse:
        new_influencer = self.influencer_repository.update_influencer(influencer_id=influencer_id,
                                                                      influencer_request=request)

        if new_influencer:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for influencer with id {}".format(influencer_id))
            return GenericResponse(success=False, button_text=None,
                                   message="No influencer found for given influencer_id")

    def create_influencer_metric(self, request: InfluencerMetricRequest) -> GenericResponse:
        timestamp_id = id_utils.get_influencer_metric_id()
        try:
            new_influencer_metric = self.influencer_repository.create_influencer_metric(timestamp_id, request)

            if new_influencer_metric:
                return GenericResponse(success=True, button_text=None, message=None)
            else:
                return GenericResponse(success=False, button_text=None,
                                       message="Unable to create new influencer_metric")
        except Exception as e:
            _log.error(
                f"Error occurred while creating new influencer_metric, influencer_metric_id: {timestamp_id}. Error: {str(e)}")
            return GenericResponse(success=False, button_text=None,
                                   message=f"Something went wrong while creating new influencer_metric, influencer_metric_id: {timestamp_id}")

    def update_influencer_metric(self, influencer_metric_id: str, request: InfluencerMetricRequest) -> GenericResponse:

        new_influencer_metric = self.influencer_repository.update_influencer_metric(
            influencer_metric_id=influencer_metric_id,
            influencer_metric_request=request)

        if new_influencer_metric:
            return GenericResponse(success=True, button_text=None, message=None)
        else:
            _log.info("No record found for influencer_metric with id {}".format(influencer_metric_id))
            return GenericResponse(success=False, button_text=None,
                                   message="No influencer_metric found for given influencer_metric_id")
