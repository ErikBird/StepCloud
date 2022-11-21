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


async def test_post_customer_device_existing_device(
        client: AsyncClient, gateway_access_token_headers: Dict[str, str], async_get_db: AsyncSession) -> None:
    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/test-token",
                          headers=gateway_access_token_headers)
    assert 200 <= r.status_code < 300
    gateway_info = r.json()
    uuid = str(gateway_info['uuid'])
    customer_device = await create_random_customer_device(db=async_get_db,
                                                          customer_office_id=gateway_info['customer_office_id'])

    payload = {
        "network_ip": "0.0.0.0",
        "registration_code": "jkljozgfg",
        "serial_number": "hkghjkkjk",
        "device_name": "Wrong_name",  # Will not be checked
        "gateway_name": customer_device.gateway_name,
        "label": "Some Label",
        "customer_office_id": customer_device.id
    }

    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/customer-device/create",
                          headers=gateway_access_token_headers, json=payload)
    assert 200 <= r.status_code < 300
    customer_device_info = r.json()
    assert customer_device_info['id'] == customer_device.id
    assert customer_device_info['gateway_name'] == customer_device.gateway_name


async def test_post_customer_device_wrong_device_name(
        client: AsyncClient, gateway_access_token_headers: Dict[str, str], async_get_db: AsyncSession) -> None:
    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/test-token",
                          headers=gateway_access_token_headers)
    assert 200 <= r.status_code < 300
    gateway_info = r.json()
    payload = {
        "network_ip": "0.0.0.0",
        "registration_code": "jkljozgfg",
        "serial_number": "hkghjkkjk",
        "device_name": "Wrong_name",
        "gateway_name": 'UniqueRandomName',
        "label": "Some Label",
        "customer_office_id": gateway_info['customer_office_id']
    }

    post_r = await client.post(f"{settings.GATEWAY_API_V1_STR}/customer-device/create",
                               headers=gateway_access_token_headers, json=payload)
    db_device = await crud.device.get_multi(db=async_get_db)
    db_identifier = await crud.identifier.get_multi(db=async_get_db)
    assert 400 <= post_r.status_code


async def test_post_customer_device(
        client: AsyncClient, gateway_access_token_headers: Dict[str, str], async_get_db: AsyncSession) -> None:
    r = await client.post(f"{settings.GATEWAY_API_V1_STR}/test-token",
                          headers=gateway_access_token_headers)
    assert 200 <= r.status_code < 300
    gateway_info = r.json()
    device_name = 'Emmi-30 HC'
    payload = {
        "network_ip": "0.0.0.0",
        "registration_code": "jkljozgfg",
        "serial_number": "hkghjkkjk",
        "device_name": device_name,
        "gateway_name": 'OtherUniqueRandomName',
        "label": "Some Label",
        "customer_office_id": gateway_info['customer_office_id']
    }

    post_r = await client.post(f"{settings.GATEWAY_API_V1_STR}/customer-device/create",
                               headers=gateway_access_token_headers, json=payload)
    assert 200 <= post_r.status_code < 300
    device_info = post_r.json()
    assert int(device_info['id'])

    db_device = await crud.device.get(id=device_info['device_id'], db=async_get_db)
    assert db_device.name == device_name
