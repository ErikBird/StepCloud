from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/", include_in_schema=False)
def redirect_docs():
    """
    Redirect to REST documentation
    :return: Redirect Response
    """
    response = RedirectResponse(url='/docs')
    return response
