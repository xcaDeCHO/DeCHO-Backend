from django.db.models.signals import post_save
from django.dispatch import receiver
from algosdk import account, mnemonic
from .models import Wallet


@receiver(post_save, sender='core.Cause')
def generate_wallet_for_cause(sender, instance, created, **kwargs):
    if created:
        private_key, address = account.generate_account()
        print(f'this is the private key {private_key}')
        print(f'this is the address {address}')
        wallet_mnemonic = mnemonic.from_private_key(private_key)
        Wallet.objects.create(address=address, mnemonic=wallet_mnemonic, cause=instance)


# TODO: Set up central wallet to transfer funds for opting in to choice






