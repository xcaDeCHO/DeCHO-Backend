import base64
from secrets import token_urlsafe

from django.db import models

# Create your models here.


class Cause(models.Model):
    STATUS = (
        ("Approved", "Approved"),
        ("pending", "pending"),
        ("done", "done"),
        ("canceled", "canceled"),
    )

    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    long_description = models.CharField(max_length=3000)
    status = models.CharField(max_length=12, choices=STATUS, default="pending")
    wallet_address = models.CharField(max_length=60)
    # uuid = models.CharField(max_length=50, blank=True, editable=False, default=token_urlsafe(15))
    photo_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.photo_url:
            self.photo_url = base64.b64encode(str(self.title).encode("ascii")).decode("ascii")
            super().save(*args, **kwargs)


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
