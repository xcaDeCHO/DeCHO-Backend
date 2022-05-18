import json
from logging import raiseExceptions
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from rest_framework import status, serializers
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .models import Cause, Giveaway, Wallet
from .serializers import CauseSerializer, GiveawaySerializer
from .signals import generate_wallet_for_cause
from .tasks import fund_wallet
from .utils import check_choice_balance, filter_transactions


@api_view(["POST"])
@throttle_classes([UserRateThrottle])
def create_cause(request):
    serializer = CauseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        with transaction.atomic():
            cause = serializer.save()
            wallet = generate_wallet_for_cause(cause)
            fund_wallet(wallet.address)
        return Response(
            {"status": status.HTTP_201_CREATED, "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    except:
        return Response(
            {
                "status": status.HTTP_424_FAILED_DEPENDENCY,
                "data": "Cause creation failed. Please try again",
            },
            status=status.HTTP_424_FAILED_DEPENDENCY,
        )


@api_view(["GET"])
def list_causes(request):
    statuses = ["pending", "Approved"]
    causes = Cause.objects.filter(status__in=statuses)
    serializer = CauseSerializer(instance=causes, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def detail_cause(request, id):
    cause = Cause.objects.filter(id=id)
    if not cause.exists():
        return Response(
            {"status": status.HTTP_404_NOT_FOUND, "detail": "Cause not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = CauseSerializer(instance=cause, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def null_causes(request):
    statuses = ["done", "canceled"]
    causes = Cause.objects.filter(status__in=statuses)
    serializer = CauseSerializer(instance=causes, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def approved_causes(request):
    causes = Cause.objects.filter(status="Approved")
    serializer = CauseSerializer(instance=causes, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def check_balances(request, address):
    balance_response = check_choice_balance(address)
    print(balance_response)
    return Response(
        {"status": status.HTTP_200_OK, "data": balance_response},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def giveaway(request, **kwargs):
    serializer = GiveawaySerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except serializers.ValidationError as err:
        return Response(
            {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": "Address could not be recorded, please confirm it's valid and try again",
                "message": err.detail
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            "status": status.HTTP_200_OK,
            "message": "Submission successfully recorded",
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def results(request, **kwargs):
    addresses = Giveaway.objects.all()
    serializer = GiveawaySerializer(instance=addresses, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data},
        status=status.HTTP_200_OK
    )


# @api_view(["GET"])
# def fund_all_wallets(request):
#     wallets = Wallet.objects.all()
#     for wallet in wallets:
#         fund_wallet(wallet.address)
#     return Response(
#         {"status": status.HTTP_200_OK, "data": "Transactions queued"}, status=status.HTTP_200_OK
#     )


def wallet_connect(request):
    address = request.GET.get("recipientAddress")
    amount = request.GET.get("amountToSend")
    request_type = request.GET.get("requestType")
    txn_method = request.GET.get("txnMethod")
    device_type = request.GET.get("deviceType")

    return render(
        request,
        "wallet_connect.html",
        {
            "address": address,
            "amount": amount,
            "request_type": request_type,
            "txn_method": txn_method,
            "device_type": device_type,
        },
    )


@api_view(['GET'])
def get_user_donations_to_cause(request, cause_id: int, address: str):
    try:
        wallet = Wallet.objects.get(cause_id=cause_id)
    except Wallet.DoesNotExist:
        return Response({"status": status.HTTP_404_NOT_FOUND, "message": "Cause wallet does not exist"},
                        status=status.HTTP_404_NOT_FOUND)
    approval_transactions = filter_transactions(from_address=address, to_address=wallet.address,
                                                asa_id=settings.CHOICE_ID)
    donation_transactions = filter_transactions(from_address=address, to_address=wallet.address)
    return Response({"status": status.HTTP_200_OK,
                     "message": {"approval_transactions": approval_transactions,
                                 "donation_transactions": donation_transactions}
                     },
                    status=status.HTTP_200_OK)
