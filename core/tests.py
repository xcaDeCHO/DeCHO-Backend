from django.test import TestCase
from molotov import scenario
# Create your tests here.

@scenario(weight=100)
async def _test_local(session):
    async with session.get("http://localhost:8000/api/v1/causes") as resp:
        assert resp.status == 200, resp.status