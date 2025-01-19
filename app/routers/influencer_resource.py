import os
from typing import Optional, List

from fastapi import APIRouter, Depends, UploadFile, File

from app.api_requests.influencer_insights import InfluencerInsights
from app.api_requests.influencer_request import InfluencerRequest
from app.api_requests.update_influencer_request import UpdateInfluencerRequest
from app.database.influencer_table import Influencer
from app.database.session import DatabaseSessionManager
from app.response.generic_response import GenericResponse
from app.response.influencer_detail import InfluencerDetail
from app.services.client_service import ClientService
from app.services.influencer_service import InfluencerService
from app.utils.logger import configure_logger

_log = configure_logger()
ALLOWED_IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/jpg"]
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]

router = APIRouter(
    prefix='/v1/influencer',
    tags=['Influencer Resource (Only For Admins)']
)

db_manager = DatabaseSessionManager()


@router.post("/create")
def create_influencer(request: InfluencerRequest, db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.create_influencer(request=request)


@router.post("/upload/image/{influencer_id}")
def create_influencer(influencer_id: int, image_file: UploadFile = File(...),
                      db=Depends(db_manager.get_db)) -> GenericResponse:
    if image_file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        return GenericResponse(success=False, status_code=400,
                               message="Invalid image type. Only JPEG, PNG, and JPG are allowed.")

    file_extension = os.path.splitext(image_file.filename)[1].lower()
    if file_extension not in ALLOWED_IMAGE_EXTENSIONS:
        return GenericResponse(success=False, status_code=400,
                               message="Invalid file extension. Only .jpg, .jpeg, .png are allowed.")

    influencer_service = InfluencerService(db)
    return influencer_service.upload_image(influencer_id=influencer_id, image_file=image_file)


@router.post("/update/{influencer_id}")
def update_influencer(influencer_id: int, request: UpdateInfluencerRequest,
                      db=Depends(db_manager.get_db)) -> GenericResponse:
    influencer_service = InfluencerService(db)
    return influencer_service.update_influencer(influencer_id=influencer_id, request=request)


@router.get("/get", response_model=None)
def get_influencer_detail(influencer_id: Optional[int] = None, phone_number: Optional[str] = None,
                          name: Optional[str] = None, insta_username: Optional[str] = None,
                          db=Depends(db_manager.get_db)) -> List[Influencer] | GenericResponse:
    # Ensure at least one search parameter is provided
    if not any([influencer_id, phone_number, name, insta_username]):
        return GenericResponse(success=False, message="At least one search parameter is required.")

    influencer_service = InfluencerService(db)
    return influencer_service.get_influencer_detail(influencer_id=influencer_id, phone_number=phone_number, name=name,
                                                    insta_username=insta_username)


@router.post('/get/insight/{influencer_id}')
def get_influencer_insight(influencer_id: int, db=Depends(db_manager.get_db)) -> InfluencerDetail | GenericResponse:
    client_service = ClientService(db)
    return client_service.get_influencer_insight(request=InfluencerInsights(client_id=2, influencer_id=influencer_id))
