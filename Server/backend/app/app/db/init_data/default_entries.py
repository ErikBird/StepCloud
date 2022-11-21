from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud, sqlmodels


async def init_default_entries(db: AsyncSession) -> None:
    log_type_label = ["error", "debug", "build"]
    visualization_type_label = ["default", "scatter", "line", "bar"]
    sensor_type_label = ["timeseries", "singular"]
    event_type_label = ["settings_changes", "performed_task"]

    for label in event_type_label:
        if not await crud.event_type.get_by_label(db=db, label=label):
            event_type_in = sqlmodels.EventTypeCreate(label=label)
            await crud.event_type.create(db=db, obj_in=event_type_in)

    for label in log_type_label:
        if not await crud.log_type.get_by_label(db=db, label=label):
            log_type_in = sqlmodels.LogTypeCreate(label=label)
            await crud.log_type.create(db=db, obj_in=log_type_in)

    for label in visualization_type_label:
        if not await crud.visualization_type.get_by_label(db=db, label=label):
            visualization_type_in = sqlmodels.VisualizationTypeCreate(label=label)
            await crud.visualization_type.create(db=db, obj_in=visualization_type_in)

    for label in sensor_type_label:
        if not await crud.sensor_type.get_by_label(db=db, label=label):
            sensor_type_in = sqlmodels.SensorTypeCreate(label=label)
            await crud.sensor_type.create(db=db, obj_in=sensor_type_in)

    default_device_supplier = await crud.device_supplier.get_by_name(db, name='default')
    if not default_device_supplier:
        device_supplier_in = sqlmodels.device_supplier.DeviceSupplierCreate(
            name='default'
        )
        default_device_supplier = await crud.device_supplier.create(db, obj_in=device_supplier_in)

    default_device = await crud.device.get_by_name(db, name='default')
    if not default_device:
        device_in = sqlmodels.device.DeviceCreate(
            name='default',
            identifiers=['*'],
            supplier_id=default_device_supplier.id
        )
        await crud.device.create_with_identifiers(db, obj_in=device_in)
