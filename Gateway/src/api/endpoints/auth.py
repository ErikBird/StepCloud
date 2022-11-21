from fastapi import APIRouter, Depends
from sqlmodel import Session

from src import sqlmodels, crud
from src.api.deps import get_session
from src.constants.const import System
from src.util.networking import get_network_interface_ip_address

router = APIRouter()


@router.get("/config", response_model=sqlmodels.Config)
def get_gateway_description():
    return sqlmodels.Config(
        uuid=System.UUID.value,
        serial_number=System.UUID.value,
        software_version=System.SOFTWARE_VERSION,
        hardware_version=System.HARDWARE_VERSION,
        authenticated=True if System.AUTH_TOKEN else False,
        network_address=get_network_interface_ip_address()
    )


@router.post("/token", response_model=sqlmodels.Config)
async def setup_token(tokens: sqlmodels.AuthTokensCreate, session: Session = Depends(get_session)):
    System.AUTH_TOKEN = crud.token.create(db=session, tokens=tokens)
    return sqlmodels.Config(
        uuid=System.UUID.value,
        serial_number=System.UUID.value,
        software_version=System.SOFTWARE_VERSION,
        hardware_version=System.HARDWARE_VERSION,
        authenticated=True if System.AUTH_TOKEN else False,
        network_address=get_network_interface_ip_address()
    )
