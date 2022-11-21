from starlette.responses import RedirectResponse
from src.api.api import api_router
from src.db.session import engine
from src.interface_manager import InterfaceManager
from src.util.logger import get_logger
from fastapi import FastAPI
import uvicorn
from src.interfaces.core_interfaces.clock import *
from src.event_bus.event_bus import EventBus
from src.constants.lifecycle_events import EventStart, EventBeforeStop, EventStop, EventBeforeLoad
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session
from src import crud

app = FastAPI(title=System.NAME)
logger = get_logger("MAIN")
# network_adapter = NetworkAdapter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
def redirect_docs():
    """
    Redirect to REST documentation
    :return: Redirect Response
    """
    response = RedirectResponse(url='/docs')
    return response


def engine_shutdown(message, code):
    """
    Callback of the engine daemon once it is ordered to shut down by the cli command 'engine stop'
    The callback needs to take care that all related Threads get stopped before they are loosing their main process
    """
    logger.debug(message)


def load_system_components():
    """
    The Method loads all integrations of the system
    """
    bus = EventBus.instance()
    InterfaceManager().register()
    bus.emit(event=EventBeforeLoad())


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def setup_uuid():
    with Session(engine) as session:
        System.UUID = crud.uuid_gateway.get_or_create(db=session)


def setup_auth_token():
    with Session(engine) as session:
        System.AUTH_TOKEN = crud.token.get(db=session)


def start():
    """
    The method emits the EventStart Event which starts the Integration Background Processes
    """
    create_db_and_tables()
    setup_uuid()
    setup_auth_token()
    load_system_components()
    EventBus.instance().emit(event=EventStart())


@app.get("/stop")
def stop():
    """
    Stops all Processes of the system gently.
    """
    EventBus.instance().emit(event=EventBeforeStop())
    EventBus.instance().stop()
    EventBus.instance().emit(event=EventStop())
    return {'status': EventBus.instance()}


if __name__ == '__main__':
    EventBus.instance().emit(event=EventBeforeLoad())
    start()
    port = 7353
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")
