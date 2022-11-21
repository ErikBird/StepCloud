from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router, tags_metadata
from app.api.admin_api_v1.api import admin_api_router, admin_tags_metadata
from app.api.gateway_api_v1.api import gateway_api_router, gateway_tags_metadata
from app.core.config import settings
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    # CORS disabled for all source domains to have no issues with any connecting device
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

adminapi = FastAPI(
    title=settings.PROJECT_NAME + '-Admin',
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=admin_tags_metadata)

adminapi.include_router(admin_api_router, prefix=settings.API_V1_STR)

app.mount("/admin", adminapi)

gatewayapi = FastAPI(
    title=settings.PROJECT_NAME + '-Gateway',
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=gateway_tags_metadata)

gatewayapi.include_router(gateway_api_router, prefix=settings.API_V1_STR)

app.mount("/gateway", gatewayapi)
