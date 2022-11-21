from fastapi import APIRouter

from .endpoints import login, user, customer, device, device_supplier, customer_device, device_event, identifier, \
    gateway, customer_office

tags_metadata = [
    {
        "name": "Authentication",
        "description": "User Login and Account Recovery",
    },
    {
        "name": "User",
        "description": "Management of the User Account. The customer has to be created by an administrator.",
    },
    {
        "name": "Device",
        "description": "Operation to access information about the supported devices",
    },
    {
        "name": "CustomerDevice",
        "description": "Manage the device instances of your account.",
    },
    {
        "name": "DeviceEvent",
        "description": "Manage the Events which occur on your devices.",
    },
    {
        "name": "Gateway",
        "description": "Manage the Gateways related to your account",
    },
    {
        "name": "CustomerOffice",
        "description": "Edit the Office Information related to your account",
    },
]
api_router = APIRouter()
api_router.include_router(login.router, tags=['Authentication'])
api_router.include_router(customer.router, prefix="/customers", tags=['User'])
api_router.include_router(user.router, prefix="/customers/users", tags=['User'])
api_router.include_router(device.router, prefix="/devices", tags=['Device'])
api_router.include_router(device_supplier.router, prefix="/devices/suppliers", tags=['Device'])
api_router.include_router(identifier.router, prefix="/devices/identifiers", tags=['Device'])
api_router.include_router(customer_device.router, prefix='/customers/devices', tags=['CustomerDevice'])
api_router.include_router(device_event.router, prefix="/customers/devices", tags=['DeviceEvent'])
api_router.include_router(gateway.router, prefix="/gateway", tags=['Gateway'])
api_router.include_router(customer_office.router, prefix='/customer-office', tags=['CustomerOffice'])
