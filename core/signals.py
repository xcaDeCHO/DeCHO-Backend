from algosdk import account, mnemonic
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cause, Wallet
from .tasks import fund_wallet


@receiver(post_save, sender=Cause)
def generate_wallet_for_cause(sender, instance, created, **kwargs):
    if created:
        private_key, address = account.generate_account()
        wallet_mnemonic = mnemonic.from_private_key(private_key)
        wallet = Wallet.objects.create(address=address, mnemonic=wallet_mnemonic, cause=instance)
        fund_wallet(wallet.address)


# TODO: Set up central wallet to transfer funds for opting in to choice
