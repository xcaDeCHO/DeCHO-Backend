from decouple import config
from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient

from .utils import decrypt_mnemonic
from core.models import Cause

fernet = settings.FERNET


# from molotov import scenario
#
#
# # Create your tests here.
#
# @scenario(weight=100)
# async def _test_local(session):
#     async with session.get("http://localhost:8000/api/v1/causes") as resp:
#         assert resp.status == 200, resp.status
#

class TestEncryption(TestCase):

    def test_encryption_and_decryption(self):
        word = "encryption"
        encrypted_word = fernet.encrypt(word.encode()).decode()
        decrypted = decrypt_mnemonic(encrypted_word)
        self.assertEqual(word, decrypted)


class TestAPI(TestCase):

    def test_successful_owner_authentication_for_cause_creation(self):
        client = APIClient()
        client.credentials(OWNER_TOKEN=config('OWNER'))
        response = client.post('/api/v1/create/',
                               data={"cause_approval": {"expiry_date": "2022-05-02T23:45:00.000Z", "goal": 10},
                                     "donations": {"expiry_date": "2022-05-02T00:00:00.000Z", "goal": 10},
                                     "title": "First Cause",
                                     "short_description": "Second cause for test",
                                     "long_description": "Long long_description gto test",
                                     "wallet_address": "QT7OZY76NQOIQWRICZNZVNK3QCUUYC4BXB7BBRHXJ3AMHDBARDGAFAXA7I",
                                     "photo_url": "https://mobile.facebook.com/Football.is.My.Life.HD/photos"
                                                  "/a.105708091455355/261385459220950/?type=3&_rdc=1&_rdr"},
                               format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cause.objects.count(), 1)

    def test_failed_owner_authentication_for_cause_creation(self):
        client = APIClient()
        client.credentials(OWNER_TOKEN='aa')
        response = client.post('/api/v1/create/',
                               data={"cause_approval": {"expiry_date": "2022-05-02T23:45:00.000Z", "goal": 10},
                                     "donations": {"expiry_date": "2022-05-02T00:00:00.000Z", "goal": 10},
                                     "title": "First Cause",
                                     "short_description": "Second cause for test",
                                     "long_description": "Long long_description gto test",
                                     "wallet_address": "QT7OZY76NQOIQWRICZNZVNK3QCUUYC4BXB7BBRHXJ3AMHDBARDGAFAXA7I",
                                     "photo_url": "https://mobile.facebook.com/Football.is.My.Life.HD/photos"
                                                  "/a.105708091455355/261385459220950/?type=3&_rdc=1&_rdr"},
                               format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Cause.objects.count(), 0)

    def test_failed_no_authentication_for_cause_creation(self):
        client = APIClient()
        response = client.post('/api/v1/create/',
                               data={"cause_approval": {"expiry_date": "2022-05-02T23:45:00.000Z", "goal": 10},
                                     "donations": {"expiry_date": "2022-05-02T00:00:00.000Z", "goal": 10},
                                     "title": "First Cause",
                                     "short_description": "Second cause for test",
                                     "long_description": "Long long_description gto test",
                                     "wallet_address": "QT7OZY76NQOIQWRICZNZVNK3QCUUYC4BXB7BBRHXJ3AMHDBARDGAFAXA7I",
                                     "photo_url": "https://mobile.facebook.com/Football.is.My.Life.HD/photos"
                                                  "/a.105708091455355/261385459220950/?type=3&_rdc=1&_rdr"},
                               format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Cause.objects.count(), 0)
