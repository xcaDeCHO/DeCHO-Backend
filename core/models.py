from django.db import models

from .utils import gen_random_photo_url
from django.conf import settings


fernet = settings.FERNET

# Create your models here.


class Cause(models.Model):
    STATUS = (
        ("Approved", "Approved"),
        ("pending", "pending"),
        ("done", "done"),
        ("canceled", "canceled"),
    )

    title = models.CharField(max_length=255)
    long_description = models.CharField(max_length=3000)
    short_description = models.CharField(max_length=255)
    status = models.CharField(max_length=12, choices=STATUS, default="pending")
    wallet_address = models.CharField(max_length=60)
    photo_url = models.URLField(default=gen_random_photo_url)
    verified = models.BooleanField(default=False)


class Wallet(models.Model):
    cause = models.OneToOneField(Cause, on_delete=models.CASCADE, related_name="decho_wallet")
    mnemonic = models.CharField(max_length=3000)
    address = models.CharField(max_length=100, unique=True)


class Donation(models.Model):
    cause = models.OneToOneField(Cause, on_delete=models.CASCADE, related_name="donations")
    expiry_date = models.DateTimeField()
    goal = models.IntegerField()


class Approval(models.Model):
    cause = models.OneToOneField(Cause, on_delete=models.CASCADE, related_name="cause_approval")
    expiry_date = models.DateTimeField()
    goal = models.IntegerField()


class Giveaway(models.Model):
    address = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.address


def encrypt_all_wallets():
    wallets = Wallet.objects.all()
    for wallet in wallets:
        encrypted_mnemonic = fernet.encrypt(wallet.mnemonic.encode()).decode()
        wallet.mnemonic = encrypted_mnemonic
        wallet.save()
