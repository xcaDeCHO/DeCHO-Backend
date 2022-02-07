from Decho.celery import app
from .models import Cause, Wallet
from .utils import check__choice_balance
from celery import shared_task
from decouple import config
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction
from django.conf import settings

algod_address = config('ALGOD_ADDRESS')
algod_token = ''

@app.task
def update_cause_status():
    causes = Cause.objects.filter(status='pending')
    for cause in causes:
        address = cause.decho_wallet.address
        balance = check__choice_balance(address)
        try:
            balance = int(balance)
        except:
            return

        if balance/100 >= cause.cause_approval.goal:
            cause.status = 'Approved'



@app.task
def opt_in_to_choice(address):
    wallet = Wallet.objects.get(address=address)
    print(wallet)
    client = algod.AlgodClient(algod_token, algod_address)
    account = client.account_info(address)
    contains_choice = False
    for asset in account["assets"]:
        if asset["asset-id"] == settings.CHOICE_ID:
            contains_choice = True
            break
    if not contains_choice:
        suggested_params = client.suggested_params()
        unsigned_transaction = transaction.AssetTransferTxn(
            wallet.address, suggested_params, wallet.address, 0, settings.CHOICE_ID
        )
        signed_transaction = unsigned_transaction.sign(mnemonic.to_private_key(wallet.mnemonic))
        transaction_id = client.send_transaction(signed_transaction)
        contains_choice = True
    print(contains_choice)
    return contains_choice


@app.task
def fund_wallet(address):
    print('fund wallet line 1')
    client = algod.AlgodClient(algod_token, algod_address)
    params = client.suggested_params()
    central_address = config('CENTRAL_WALLET_ADDRESS')
    unsigned_txn = transaction.PaymentTxn(central_address, params, address, 100000, None, '')
    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(config('CENTRAL_MNEMONIC')))
    txid = client.send_transaction(signed_txn)
    print(txid)
    try:
        confirmed_txn = transaction.wait_for_confirmation(client, txid, 4)
        opt_in_to_choice.delay(address)
    except Exception as err:
        print(err)
        return



# @app.task
# def opt_in_to_choice(address):
#     wallet = Wallet.objects.get(address=address)
#     client = algod.AlgodClient(algod_token, algod_address)
#     suggested_params = client.suggested_params()
#     unsigned_transaction = transaction.AssetTransferTxn(
#         wallet.address, suggested_params, wallet.address, 0, settings.CHOICE_ID
#     )
#     signed_transaction = unsigned_transaction.sign(mnemonic.to_private_key(wallet.mnemonic))
#     transaction_id = client.send_transaction(signed_transaction)

# from django.db import models
# from django.template.defaultfilters import slugify
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=30)
#     description = models.CharField(max_length=300)
#
#
# class Article(models.Model):
#     name = models.CharField(max_length=30)
#     body = models.CharField(max_length=5000)
#     image = models.ImageField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)