from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CauseSerializer
from .models import Cause, Wallet
from .utils import check__choice_balance
from .tasks import fund_wallet


# Create your views here.

@api_view(['POST'])
def create_cause(request):
    serializer = CauseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'status': status.HTTP_201_CREATED, 'data': serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_causes(request):
    causes = Cause.objects.all()
    cause_address = causes[1].decho_wallet.address
    serializer = CauseSerializer(instance=causes, many=True)
    return Response({'status': status.HTTP_200_OK, 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def check_balances(request, address):
    balance_response = check__choice_balance(address)
    print(balance_response)
    return Response(balance_response, status=balance_response.get('status'))


@api_view(['GET'])
def fund_all_wallets(request):
    wallets = Wallet.objects.all()
    for wallet in wallets:
        fund_wallet.delay(wallet.address)
    return Response({'status': status.HTTP_200_OK, 'data': 'Transactions queued'}, status=status.HTTP_200_OK)