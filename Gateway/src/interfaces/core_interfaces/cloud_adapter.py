import json

import requests
from fastapi.encoders import jsonable_encoder
from requests.structures import CaseInsensitiveDict
from sqlmodel import Session
from starlette import status
from datetime import datetime
from src import crud
from src.constants.const import ProcessMode, System, RequestedType, EventTypeEnum
from src.db.session import engine
from src.event_bus.decorator import subscribe
from src.event_bus.helper_classes import Event
from src.interfaces.abstract_interface import SystemInterface
from src import sqlmodels


class EventUploadData(Event):
    def __init__(self, cloud_id,
                 event_type: EventTypeEnum,
                 sensor_data: list[sqlmodels.SensorData] = None,
                 log_data: list[sqlmodels.LogData] = None,
                 setting_data: list[sqlmodels.SettingData] = None):
        super().__init__(name='EventUploadData')
        self.time_recorded = datetime.utcnow().isoformat()
        self.sensor_data: list[sqlmodels.SensorData] = sensor_data
        self.log_data: list[sqlmodels.LogData] = log_data
        self.setting_data: list[sqlmodels.SettingData] = setting_data
        self._cloud_id = cloud_id
        self._event_type = event_type

    @property
    def sender_cloud_id(self):
        return self._cloud_id

    def json(self):
        json = {'event_type': self._event_type,
                'time_recorded': self.time_recorded,
                'customer_device_id': self._cloud_id,
                "gateway_uuid": System.UUID.value}
        if self.sensor_data:
            json["sensor_data"] = self.sensor_data
        if self.log_data:
            json["log_data"] = self.log_data
        if self.setting_data:
            json["setting_data"] = self.setting_data
        return json


class CloudAdapter(SystemInterface):
    """
    """

    def __init__(self):
        super().__init__('CloudAdapter')
        self.cloud_url = 'http://localhost'
        self.buffered_data = False

    @subscribe(process_mode=ProcessMode.ASYNC, on_event=EventUploadData)
    async def upload_event_data(self, event):
        if not event.sender_cloud_id:
            self.logger.exception('Sender is missing the cloud_id -> the event is not uploaded!')
            return
        path = '/gateway/api/v1/event/create'
        self.logger.info(f'Try to POST data to {path}')
        await self.request(data=event.json(), url=path, method=RequestedType.POST)

    def upload_buffer(self):
        self.logger.info('Upload buffered Data')
        with Session(engine) as session:
            request_buffer = crud.post_request.get_all(db=session)
            self.buffered_data = False
            # Needs to be deleted before the requests because the upload might insert new database values if they fail
            crud.post_request.delete_all(db=session)
            self.logger.info('Send stored POST requests to server')
            for post_request in request_buffer:
                self.request(method=RequestedType.POST, url=post_request.target, data=post_request.data)

    def get_access_token_header(self):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        if System.AUTH_TOKEN:
            headers["Authorization"] = f"Bearer {System.AUTH_TOKEN.access_token}"
        return headers

    async def refresh_token(self):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {System.AUTH_TOKEN.refresh_token}"
        r = requests.post(url=f'{self.cloud_url}/gateway/api/v1/refresh',
                          headers=headers)
        assert r.status_code == 200
        with Session(engine) as session:
            crud.token.update(db=session, access_token=r.json()['access_token'])

    async def request(self, method: RequestedType, url: str, data=None):
        try:
            r = requests.request(method, url=self.cloud_url + url, json=jsonable_encoder(data),
                                 headers=self.get_access_token_header())
            if r.status_code == status.HTTP_401_UNAUTHORIZED:
                self.logger.debug('AccessToken needs to be refreshed')
                await self.refresh_token()
                r = requests.request(method, url=self.cloud_url + url, json=jsonable_encoder(data),
                                     headers=self.get_access_token_header())

            if self.buffered_data:
                self.upload_buffer()
            return r
        except (requests.ConnectionError, requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError) as e:
            if method is RequestedType.POST:
                self.buffered_data = True
                with Session(engine) as session:
                    data_as_string: str = json.dumps(jsonable_encoder(data))
                    request_model = sqlmodels.PostRequestCreate(target=url, data=data_as_string)
                    crud.post_request.create(post_request_in=request_model, db=session)
                self.logger.debug('%s - Data is stored in the database.', str(e))
            # Else: self.logger.exception(e)
        except Exception as e:
            self.logger.error(e)

    async def get_customer_devices(self):
        r = await self.request(method=RequestedType.GET, url='/gateway/api/v1/customer-device/all')
        if r:
            return r.json()
        else:
            return []

    '''
    @subscribe(process_mode=ProcessMode.ASYNC, on_event=EventUploadData)
    def send_ui_messages(self, event: EventUploadData):
        # self.cloud_logger.info(event.json)
        # self.UI_queue.put_nowait(event.json)
        pass'''
