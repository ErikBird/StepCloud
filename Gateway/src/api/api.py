from fastapi import APIRouter
from .endpoints import interface, auth, event, util, log

admin_tags_metadata = [
    {
        "name": "Interfaces",
        "description": "Management of the Gateway Interfaces.",
    },
    {
        "name": "Authentication",
        "description": "Operation to setup the Gateway Authentication for the cloud.",
    },
    {
        "name": "Events",
        "description": "Listen to the Events occurring on the Gateway",
    },
    {
        "name": "Utilities",
        "description": "Utilities",
    },
]
api_router = APIRouter()

api_router.include_router(interface.router, prefix="/interface", tags=['Interfaces'])
api_router.include_router(auth.router, prefix="/auth", tags=['Authentication'])
api_router.include_router(event.router, prefix="/events", tags=['Events'])
api_router.include_router(util.router, tags=['Utilities'])
api_router.include_router(log.router, prefix="/log", tags=['Log'])
