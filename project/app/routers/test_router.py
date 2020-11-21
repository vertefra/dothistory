from fastapi import APIRouter, Depends
from project.app.config import get_settings, Settings

router = APIRouter()


@router.get('/ping')
def ping(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong",
        "environment": settings.environment
    }
