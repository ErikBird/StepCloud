# Databse Design

```mermaid
classDiagram
direction BT
class alembic_version {
   varchar(32) version_num
}
class customer {
   varchar name
   varchar vat_id
   integer contract_level
   integer id
}
class customerdevice {
   varchar network_ip
   varchar registration_code
   varchar serial_number
   varchar name
   integer device_id
   integer customer_id
   boolean monitoring
   integer id
}
class device {
   varchar name
   integer supplier_id
   integer id
}
class deviceevent {
   timestamp with time zone time_recorded
   integer customer_device_id
   integer id
}
class devicesupplier {
   varchar name
   integer id
}
class identifier {
   integer device_id
   varchar expression
}
class logdata {
   json data
   varchar label
   integer event_id
   integer log_type_id
   integer id
}
class logtype {
   varchar label
   integer id
}
class sensordata {
   json data
   varchar label
   varchar unit
   integer event_id
   integer sensor_type_id
   integer visualization_type_id
   integer id
}
class sensortype {
   varchar label
   integer id
}
class settingdata {
   json data
   varchar label
   integer event_id
   integer id
}
class user {
   varchar email
   boolean is_active
   boolean is_superuser
   varchar first_name
   varchar last_name
   integer customer_id
   varchar hashed_password
   integer id
}
class visualizationtype {
   varchar label
   integer id
}

customer  -->  customerdevice 
device  -->  customerdevice 
devicesupplier  -->  device
customerdevice  -->  deviceevent 
device  -->  identifier 
deviceevent  -->  logdata 
logtype  -->  logdata 
deviceevent  -->  sensordata 
sensortype  -->  sensordata  
visualizationtype  -->  sensordata 
deviceevent  -->  settingdata 
customer  -->  user 

```

## Reasoning

### User

The user e-mail has to be unique to query easily for a login.

## Inspiration

https://towardsdatascience.com/building-and-leveraging-an-event-based-data-model-for-analyzing-online-data-c166c523fe6a
https://medium.com/@tobyhede/event-sourcing-with-postgresql-28c5e8f211a2
https://softwaremill.com/implementing-event-sourcing-using-a-relational-database/
