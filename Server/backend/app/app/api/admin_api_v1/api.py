from fastapi import APIRouter, Depends
from app.api import deps
from .endpoints import user, customer, device, device_supplier, customer_device, device_event, identifier, \
    customer_office

admin_tags_metadata = [
    {
        "name": "User",
        "description": "Management of the User Accounts.",
    },
    {
        "name": "Device",
        "description": "Operation to access information about the supported devices",
    },
    {
        "name": "CustomerDevices",
        "description": "Manage the device instances.",
    },
    {
        "name": "DeviceEvent",
        "description": "Manage the Events.",
    },
    {
        "name": "CustomerOffice",
        "description": "Manage the Offices of Customers.",
    },
]

admin_api_router = APIRouter(
    dependencies=[Depends(deps.get_current_active_superuser)],
)

admin_api_router.include_router(customer.router, prefix="/customers", tags=['User'])
admin_api_router.include_router(user.router, prefix="/customers/users", tags=['User'])
admin_api_router.include_router(device.router, prefix="/devices", tags=['Device'])
admin_api_router.include_router(device_supplier.router, prefix="/devices/suppliers", tags=['Device'])
admin_api_router.include_router(identifier.router, prefix="/devices/identifiers", tags=['Device'])
admin_api_router.include_router(customer_device.router, tags=['CustomerDevices'])
admin_api_router.include_router(device_event.router, tags=["DeviceEvent"])
admin_api_router.include_router(customer_office.router, prefix="/customer-office", tags=['CustomerOffice'])
