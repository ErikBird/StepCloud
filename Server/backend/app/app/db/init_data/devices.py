from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud, sqlmodels


async def init_devices(db: AsyncSession) -> None:
    names = [('ASIGA', 'MAX UV385', 'ASIGA/MAX.png'),
             ('ASIGA', 'MAX Mini', 'default.png'),
             ('ASIGA', 'PRO 2 UV385', 'default.png'),
             ('ASIGA', 'MAX UV365', 'ASIGA/MAX.png'),
             ('ASIGA', 'PRO 4K UV385', 'ASIGA/4K.png'),
             ('EMAG', 'Emmi-30 HC', 'EMAG/emmi_30hc.png'),
             ('NK-Optik', 'Otoflash G171', 'NK-Optik/Otoflash_G171.png')]

    for supplier_name, device_name, image_path in names:
        supplier = await crud.device_supplier.get_by_name(db, name=supplier_name)
        if not supplier:
            device_supplier_in = sqlmodels.device_supplier.DeviceSupplierCreate(
                name=supplier_name
            )
            supplier = await crud.device_supplier.create(db, obj_in=device_supplier_in)

        if not await crud.device.get_by_name(db, name=device_name):
            device_in = sqlmodels.device.DeviceCreate(
                image_path=image_path,
                name=device_name,
                identifiers=[device_name],
                supplier_id=supplier.id
            )
            await crud.device.create_with_identifiers(db, obj_in=device_in)
