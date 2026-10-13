from fastapi import APIRouter
from backend.api import health, playbook, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(playbook.router, prefix="/api", tags=["playbook"])
api_router.include_router(ui.router, tags=["ui"])
