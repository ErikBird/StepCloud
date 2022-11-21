from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr
import requests
from app import sqlmodels
from app.api import deps
from app.utils import send_test_email

router = APIRouter()


@router.post("/test-celery/", status_code=201)
def test_celery(
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    # celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", status_code=201)
def test_email(
        email_to: EmailStr,
        current_user: sqlmodels.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
