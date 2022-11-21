from fastapi import APIRouter

from .endpoints import device_event, auth, customer_device

gateway_tags_metadata = [
    {
        "name": "DeviceEvent",
        "description": "Post the Events that are collected with the gateway",
    },
    {
        "name": "Authentication",
        "description": "Gateway authentication endpoints on the server",
    },
    {
        "name": "CustomerDevice",
        "description": "Create Customer Devices",
    },
]
gateway_api_router = APIRouter()
gateway_api_router.include_router(device_event.router, prefix="/event", tags=['DeviceEvent'])
gateway_api_router.include_router(auth.router, tags=['Authentication'])
gateway_api_router.include_router(customer_device.router, prefix="/customer-device", tags=['CustomerDevice'])
