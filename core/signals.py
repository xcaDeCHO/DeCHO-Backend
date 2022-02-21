from algosdk import account, mnemonic
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Cause, Wallet
from .tasks import fund_wallet

fernet = settings.FERNET


def generate_wallet_for_cause(instance: Cause):
    private_key, address = account.generate_account()
    wallet_mnemonic = mnemonic.from_private_key(private_key)
    encrypted_mnemonic = fernet.encrypt(wallet_mnemonic.encode()).decode()
    wallet = Wallet.objects.create(address=address, mnemonic=encrypted_mnemonic, cause=instance)
    return wallet

# TODO: Set up central wallet to transfer funds for opting in to choice
