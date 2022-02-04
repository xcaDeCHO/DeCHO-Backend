from rest_framework import serializers
from .models import Cause, Wallet, Donation, Approval
from secrets import token_urlsafe
from .utils import check__choice_balance


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['address']


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['expiry_date', 'goal']


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ['expiry_date', 'goal']


class CauseSerializer(serializers.ModelSerializer):
    cause_approval = ApprovalSerializer()
    donations = DonationSerializer()
    decho_wallet = WalletSerializer(read_only=True)
    wallet_address = serializers.CharField(write_only=True)
    balance = serializers.SerializerMethodField()

    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Cause
        fields = '__all__'

    def create(self, validated_data):
        data = validated_data.copy()
        approval = data.pop('cause_approval')
        donation = data.pop('donations')
        cause = Cause.objects.create(**data)
        Approval.objects.create(cause=cause, **approval)
        Donation.objects.create(cause=cause, **donation)
        return cause

    def get_photo_url(self, obj):
        # return f"https://avatars.dicebear.com/api/bottts/{token_urlsafe(10)}.svg"
        return "https://picsum.photos/350/350"

    def get_balance(self, instance):
        balance = check__choice_balance(instance.decho_wallet.address)
        return balance
