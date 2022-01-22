from django.db.models.signals import post_save
from django.dispatch import receiver
from algosdk import account, mnemonic
from .models import Wallet, Cause


@receiver(post_save, sender=Cause)
def generate_wallet_for_cause(sender, instance, created, **kwargs):
    if created:
        private_key, address = account.generate_account()
        wallet_mnemonic = mnemonic.from_private_key(private_key)
        Wallet.objects.create(address=address, mnemonic=wallet_mnemonic, cause=instance)

# TODO: Set up central wallet to transfer funds for opting in to choice
