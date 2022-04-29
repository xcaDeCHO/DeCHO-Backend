from django.conf import settings
from rest_framework import serializers

from .models import Approval, Cause, Donation, Giveaway, Wallet
from .tasks import opt_in_to_choice
from .utils import check_algo_balance, check_choice_balance

algod_client = settings.ALGOD_CLIENT


class GiveawaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Giveaway
        fields = ["address"]


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["address"]


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ["expiry_date", "goal"]


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ["expiry_date", "goal"]


class CauseSerializer(serializers.ModelSerializer):
    cause_approval = ApprovalSerializer()
    donations = DonationSerializer()
    decho_wallet = WalletSerializer(read_only=True)
    wallet_address = serializers.CharField(write_only=True, max_length=58, min_length=58)
    balance = serializers.SerializerMethodField()
    verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = Cause
        fields = "__all__"

    def create(self, validated_data):
        data = validated_data.copy()
        approval = data.pop("cause_approval")
        donation = data.pop("donations")
        cause = Cause.objects.create(**data)
        Approval.objects.create(cause=cause, **approval)
        Donation.objects.create(cause=cause, **donation)
        return cause

    def get_balance(self, instance):
        if instance.status == "pending":
            balance = check_choice_balance(instance.decho_wallet.address)
        else:
            balance = check_algo_balance(instance.decho_wallet.address)

        return balance

