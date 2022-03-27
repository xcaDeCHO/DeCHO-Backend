from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .models import Cause, Giveaway
from .serializers import CauseSerializer, GiveawaySerializer
from .signals import generate_wallet_for_cause
from .tasks import fund_wallet
from .utils import check_choice_balance


@api_view(["POST"])
@throttle_classes([UserRateThrottle])
@transaction.atomic
def create_cause(request):
    serializer = CauseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    cause = serializer.save()
    wallet = generate_wallet_for_cause(cause)
    fund_wallet(wallet.address)
    return Response(
        {"status": status.HTTP_201_CREATED, "data": serializer.data},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def list_causes(request):
    statuses = ["pending", "Approved"]
    causes = Cause.objects.filter(status__in=statuses)
    serializer = CauseSerializer(instance=causes, many=True)
    return Response(
        {headers: {"Access-Control-Allow-Origin": "*"}, "status": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def null_causes(request):
    statuses = ["done", "canceled"]
    causes = Cause.objects.filter(status__in=statuses)
    serializer = CauseSerializer(instance=causes, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK
    )


# TODO: Write view for canceled causes


@api_view(["GET"])
def approved_causes(request):
    causes = Cause.objects.filter(status="Approved")
    serializer = CauseSerializer(instance=causes, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def check_balances(request, address):
    balance_response = check_choice_balance(address)
    print(balance_response)
    return Response(
        {"status": status.HTTP_200_OK, "data": balance_response}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def giveaway(request, **kwargs):
    serializer = GiveawaySerializer(data=request.data)
    try:
        serializer.is_valid()
        serializer.save()
    except AssertionError:
        return Response(
            {"status": status.HTTP_409_CONFLICT, "data": "This address has already been recorded"},
            status=status.HTTP_409_CONFLICT,
        )
    return Response(
        {"status": status.HTTP_200_OK, "data": "Submission Successfully Recorded"},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def results(request, **kwargs):
    addresses = Giveaway.objects.all()
    serializer = GiveawaySerializer(instance=addresses, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK
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
