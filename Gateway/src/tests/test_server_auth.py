import pytest
import requests

from src.constants.const import System

pytestmark = pytest.mark.asyncio


async def test_activate_interface():
    r = requests.post(url='http://localhost/gateway/api/v1/test-token',
                      headers={'Authentication': f'Bearer {System.AUTH_TOKEN.access_token}'})
    assert r.status_code == 200
