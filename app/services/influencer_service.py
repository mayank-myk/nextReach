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
        new_influencer = self.influencer_repository.create_influencer(timestamp_id, request)

        if new_influencer:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None, error_message="Unable to create new influencer")

    def update_influencer(self, influencer_id: str, request: InfluencerRequest) -> GenericResponse:
        new_influencer = self.influencer_repository.update_influencer(influencer_id=influencer_id,
                                                                      influencer_request=request)

        if new_influencer:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None,
                                   error_message="No influencer found for given influencer_id")

    def create_influencer_metric(self, request: InfluencerMetricRequest) -> GenericResponse:
        timestamp_id = id_utils.get_influencer_metric_id()
        new_influencer_metric = self.influencer_repository.create_influencer_metric(timestamp_id, request)

        if new_influencer_metric:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None,
                                   error_message="Unable to create new influencer metric")

    def update_influencer_metric(self, influencer_metric_id: str, request: InfluencerMetricRequest) -> GenericResponse:

        new_influencer_metric = self.influencer_repository.update_influencer_metric(
            influencer_metric_id=influencer_metric_id,
            influencer_metric_request=request)

        if new_influencer_metric:
            return GenericResponse(success=True, error_code=None, error_message=None)
        else:
            return GenericResponse(success=False, error_code=None,
                                   error_message="No influencer_metric found for given influencer_metric_id")
