from app.tests.utils.user import create_random_customer
from sqlmodel.ext.asyncio.session import AsyncSession
import pytest
from app import sqlmodels, crud
from app.tests.utils.customer_device import create_random_customer_device
from app.tests.utils.device_event import create_random_device_event
from datetime import datetime
import logging

from app.tests.utils.customer_office import create_random_customer_office
from app.tests.utils.gateway import create_random_gateway

pytestmark = pytest.mark.asyncio


async def test_create_simple_device_event(async_get_db: AsyncSession) -> None:
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    gateway = await create_random_gateway(db=async_get_db, customer_office_id=customer_office.id)
    customer_device = await create_random_customer_device(db=async_get_db, customer_office_id=customer_office.id,
                                                          customer_id=customer.id, gateway_id=gateway.uuid)
    device_event_in = sqlmodels.DeviceEventCreate(
        event_type=sqlmodels.EventTypeEnum.performed_task,
        gateway_uuid=gateway.uuid,
        time_recorded=datetime.utcnow(),
        customer_device_id=customer_device.id)
    device_event = await crud.device_event.create(db=async_get_db, obj_in=device_event_in)
    assert device_event
    assert int(device_event.id)


async def test_create_settings_data(async_get_db: AsyncSession) -> None:
    device_event = await create_random_device_event(db=async_get_db)
    data = {'data': [1, 2, 3, 4, 5, 6, 7, 8]}
    label = 'test_data'
    obj_in_settings_data = sqlmodels.SettingDataCreate(label=label,
                                                       data=data,
                                                       event_id=device_event.id)
    settings_data = await crud.settings_data.create(db=async_get_db, obj_in=obj_in_settings_data)

    assert settings_data
    assert int(settings_data.id)

    settings_data = await crud.settings_data.get_by_event_id(db=async_get_db, device_event_id=device_event.id)

    assert settings_data
    assert len(settings_data) > 0
    assert int(settings_data[0].id)
    assert settings_data[0].data == data
    assert settings_data[0].label == label


async def test_create_settings_device_event(async_get_db: AsyncSession) -> None:
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    customer_device = await create_random_customer_device(db=async_get_db, customer_office_id=customer_office.id,
                                                          customer_id=customer.id)
    gateway = await create_random_gateway(db=async_get_db, customer_office_id=customer_office.id)

    now = datetime.utcnow()
    data = {'data': [1, 2, 3, 4, 5, 6, 7, 8]}
    label = 'test_data'
    settings_data = sqlmodels.SettingDataCreate(label=label,
                                                data=data)
    device_event_in = sqlmodels.DeviceEventCreate(
        event_type=sqlmodels.EventTypeEnum.performed_task,
        time_recorded=now,
        gateway_uuid=gateway.uuid,
        customer_device_id=customer_device.id,
        setting_data=[settings_data])
    device_event = await crud.device_event.create(db=async_get_db, obj_in=device_event_in)
    assert device_event
    assert int(device_event.id)

    settings_data = await crud.settings_data.get_by_event_id(db=async_get_db, device_event_id=device_event.id)
    assert settings_data
    assert len(settings_data) > 0
    assert settings_data[0].data == data
    assert settings_data[0].label == label


async def test_get_log_type_by_label(async_get_db: AsyncSession) -> None:
    for log_type_label in ['debug', 'error', 'build']:
        log_type = await crud.log_type.get_by_label(db=async_get_db, label=log_type_label)
        assert log_type
        assert int(log_type.id)
        assert log_type.label == log_type_label


async def test_create_log_data(async_get_db: AsyncSession) -> None:
    device_event = await create_random_device_event(db=async_get_db)
    data = {'data': [1, 2, 3, 4, 5, 6, 7, 8]}
    label = 'test_data'
    log_type = 'debug'
    obj_in_log_data = sqlmodels.LogDataCreate(label=label,
                                              data=data,
                                              event_id=device_event.id,
                                              log_type=log_type)
    log_data = await crud.log_data.create(db=async_get_db, obj_in=obj_in_log_data)

    assert log_data
    assert int(log_data.id)

    log_data = await crud.log_data.get_by_event_id(db=async_get_db, device_event_id=device_event.id)

    assert log_data
    assert len(log_data) > 0
    assert int(log_data[0].id)
    assert log_data[0].data == data
    assert log_data[0].label == label


async def test_create_log_device_event(async_get_db: AsyncSession) -> None:
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    customer_device = await create_random_customer_device(db=async_get_db, customer_office_id=customer_office.id,
                                                          customer_id=customer.id)
    gateway = await create_random_gateway(db=async_get_db, customer_office_id=customer_office.id,
                                          customer_id=customer.id)
    now = datetime.utcnow()
    data = {'data': [1, 2, 3, 4, 5, 6, 7, 8]}
    label = 'test_data'
    log_type = 'debug'
    log_data = sqlmodels.LogDataCreate(label=label,
                                       log_type=log_type,
                                       data=data)

    device_event_in = sqlmodels.DeviceEventCreate(
        event_type=sqlmodels.EventTypeEnum.performed_task,
        time_recorded=now,
        gateway_uuid=gateway.uuid,
        customer_device_id=customer_device.id,
        log_data=[log_data])
    device_event = await crud.device_event.create(db=async_get_db, obj_in=device_event_in)
    assert device_event
    assert int(device_event.id)

    log_data = await crud.log_data.get_by_event_id(db=async_get_db, device_event_id=device_event.id)

    assert log_data
    assert len(log_data) > 0
    assert int(log_data[0].id)
    assert log_data[0].data == data
    assert log_data[0].label == label


async def test_get_sensor_type_by_label(async_get_db: AsyncSession) -> None:
    for sensor_type_label in ['singular', 'timeseries']:
        sensor_type = await crud.sensor_type.get_by_label(db=async_get_db, label=sensor_type_label)
        assert sensor_type
        assert int(sensor_type.id)
        assert sensor_type.label == sensor_type_label


async def test_get_visualization_type_by_label(async_get_db: AsyncSession) -> None:
    for visualization_type_label in ['default', 'scatter', 'line', 'bar']:
        visualization_type = await crud.visualization_type.get_by_label(db=async_get_db, label=visualization_type_label)
        assert visualization_type
        assert int(visualization_type.id)
        assert visualization_type.label == visualization_type_label


async def test_create_sensor_data(async_get_db: AsyncSession) -> None:
    device_event = await create_random_device_event(db=async_get_db)
    data = {'data': [1, 2, 3, 4, 5, 6, 7, 8]}
    label = 'test_data'
    visualization_type = 'default'
    sensor_type = 'timeseries'
    obj_in_sensor_data = sqlmodels.SensorDataCreate(label=label,
                                                    data=data,
                                                    event_id=device_event.id,
                                                    sensor_type=sensor_type,
                                                    visualization_type=visualization_type)
    sensor_data = await crud.sensor_data.create(db=async_get_db, obj_in=obj_in_sensor_data)

    assert sensor_data
    assert int(sensor_data.id)

    sensor_data = await crud.sensor_data.get_by_event_id(db=async_get_db, device_event_id=device_event.id)

    assert sensor_data
    assert len(sensor_data) > 0
    assert int(sensor_data[0].id)
    assert sensor_data[0].data == data
    assert sensor_data[0].label == label


async def test_create_sensor_device_event(async_get_db: AsyncSession) -> None:
    customer = await create_random_customer(db=async_get_db)
    customer_office = await create_random_customer_office(db=async_get_db, customer_id=customer.id)
    customer_device = await create_random_customer_device(db=async_get_db, customer_office_id=customer_office.id,
                                                          customer_id=customer.id)
    gateway = await create_random_gateway(db=async_get_db, customer_office_id=customer_office.id)
    now = datetime.utcnow()
    data = {'data': [1, 2, 3, 4, 5, 6, 7, 8]}
    label = 'test_data'
    visualization_type = 'default'
    sensor_type = 'timeseries'
    sensor_data = sqlmodels.SensorDataCreate(label=label,
                                             data=data,
                                             sensor_type=sensor_type,
                                             visualization_type=visualization_type)
    device_event_in = sqlmodels.DeviceEventCreate(event_type=sqlmodels.EventTypeEnum.performed_task,
                                                  time_recorded=now,
                                                  gateway_uuid=gateway.uuid,
                                                  customer_device_id=customer_device.id,
                                                  sensor_data=[sensor_data])
    device_event = await crud.device_event.create(db=async_get_db, obj_in=device_event_in)
    assert device_event
    assert int(device_event.id)

    sensor_data = await crud.sensor_data.get_by_event_id(db=async_get_db, device_event_id=device_event.id)

    assert sensor_data
    assert len(sensor_data) > 0
    assert int(sensor_data[0].id)
    assert sensor_data[0].data == data
    assert sensor_data[0].label == label
