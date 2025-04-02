from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.database.session import DatabaseSessionManager
from app.services.web_service import WebService
from app.utils.logger import configure_logger

_log = configure_logger()

router = APIRouter(
    prefix='/v1/health',
    tags=['Health Check Resources (For Azure)']
)

db_manager = DatabaseSessionManager()


@router.get('/check')
def run_system_health_check(db=Depends(db_manager.get_db)) -> JSONResponse:
    web_service = WebService(db)
    return None
