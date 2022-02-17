from django.db import transaction

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cause, Wallet
from .serializers import CauseSerializer
from .tasks import fund_wallet
from .utils import check_choice_balance
from .signals import generate_wallet_for_cause


# Create your views here.


@api_view(["POST"])
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
    statuses = ['pending', 'Approved']
    causes = Cause.objects.filter(status__in=statuses)
    serializer = CauseSerializer(instance=causes, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK
    )


# TODO: Write view for canceled causes

@api_view(["GET"])
def approved_causes(request):
    causes = Cause.objects.filter(status='Approved')
    serializer = CauseSerializer(instance=causes, many=True)
    return Response(
        {"status": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def check_balances(request, address):
    balance_response = check_choice_balance(address)
    print(balance_response)
    return Response(balance_response, status=balance_response.get("status"))


@api_view(["GET"])
def fund_all_wallets(request):
    wallets = Wallet.objects.all()
    for wallet in wallets:
        fund_wallet(wallet.address)
    return Response(
        {"status": status.HTTP_200_OK, "data": "Transactions queued"}, status=status.HTTP_200_OK
    )
