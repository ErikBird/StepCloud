from typing import Dict
import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from app import crud
from app.core.config import settings
import logging

from app.tests.utils.customer_device import create_random_customer_device

pytestmark = pytest.mark.asyncio


async def test_post_device_event(
        client: AsyncClient, gateway_access_token_headers: Dict[str, str], async_get_db: AsyncSession) -> None:
    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/test-token",
                          headers=gateway_access_token_headers)
    assert 200 <= r.status_code < 300
    gateway_info = r.json()
    uuid = str(gateway_info['uuid'])
    customer_device = await create_random_customer_device(db=async_get_db,
                                                          customer_office_id=gateway_info['customer_office_id'])
    payload = {
        "gateway_uuid": uuid,
        "time_recorded": datetime.utcnow().isoformat(),
        "customer_device_id": customer_device.id,
        "sensor_data": [
            {
                "label": "Separation weight limit",
                "data": {'data': [1, 2, 3, 4, 5]},
                "unit": "kg",
                "sensor_type": "timeseries",
                "visualization_type": "line"
            }
        ]
    }
    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/event/create",
                          headers=gateway_access_token_headers,
                          json=payload)

    device_event = r.json()
    assert 200 <= r.status_code < 300
    assert int(device_event['id'])
