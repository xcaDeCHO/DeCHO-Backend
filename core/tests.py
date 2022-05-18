from django.test import TestCase
from django.conf import settings
from .utils import decrypt_mnemonic


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



