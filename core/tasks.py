import logging

from algosdk import account, constants, mnemonic
from algosdk.future import transaction
from Decho.settings.common import CHOICE_ID
from decouple import config
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task, task

from .models import Cause, Wallet
from .utils import (
    check_choice_balance,
    contains_choice_coin,
    get_transactions,
    wait_for_transaction_confirmation,
)

algod_client = settings.ALGOD_CLIENT
indexer_client = settings.INDEXER_CLIENT

logger = logging.getLogger("huey")


@task()
def test_huey():
    print("This is just a test")


# Two retries might be too much
@task(retries=2)
def fund_wallet(wallet_address):
    logger.info(f"Funding wallet {wallet_address}...")

    suggested_params = algod_client.suggested_params()
    central_address = config("CENTRAL_WALLET_ADDRESS")
    unsigned_txn = transaction.PaymentTxn(
        central_address, suggested_params, wallet_address, 300000, None, ""
    )
    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(config("CENTRAL_MNEMONIC")))
    txid = algod_client.send_transaction(signed_txn)

    wait_for_transaction_confirmation(algod_client, txid)
    logger.info(f"Funded wallet successfully! {wallet_address}")

    opt_in_to_choice(wallet_address)


@db_periodic_task(crontab(minute="*/30"))
def update_cause_status():
    logger.info("Attempting to update causes status...")

    causes = Cause.objects.filter(status="pending")
    logger.info(f"Found {causes.count()} causes pending!")
    for cause in causes:
        address = cause.decho_wallet.address
        balance = check_choice_balance(address)
        try:
            balance = int(balance)
        except:
            return

        if balance / 100 >= cause.cause_approval.goal:
            cause.status = "Approved"
            transactions = get_transactions(indexer_client, address, CHOICE_ID)
            for _transaction in transactions:
                refund_from_approval(
                    wallet=cause.decho_wallet,
                    reciever=_transaction.get("sender"),
                    amount=int(_transaction.get("asset-transfer-transaction").get("amount")),
                    asset=settings.CHOICE_ID,
                )


@db_task(retries=2)
def opt_in_to_choice(address):
    logger.info(f"Opting into $CHOICE ASA for {address}...")

    wallet = Wallet.objects.get(address=address)
    if not contains_choice_coin(algod_client, address):
        suggested_params = algod_client.suggested_params()
        unsigned_transaction = transaction.AssetTransferTxn(
            wallet.address, suggested_params, wallet.address, 0, settings.CHOICE_ID
        )
        signed_transaction = unsigned_transaction.sign(mnemonic.to_private_key(wallet.mnemonic))
        transaction_id = algod_client.send_transaction(signed_transaction)

        wait_for_transaction_confirmation(algod_client, transaction_id)

    logger.info(f"Opted into $CHOICE ASA for {address} successful!")


@db_task()
def refund_from_approval(decho_wallet_addr, reciever_addr, amount, asset):
    logger.info(
        f"Refunding approval deposit of {amount} from {decho_wallet_addr} to {reciever_addr}..."
    )
    wallet = Wallet.objects.get(address=decho_wallet_addr)
    suggested_params = algod_client.suggested_params()
    txn = transaction.AssetTransferTxn(
        sender=wallet.address,
        sp=suggested_params,
        receiver=reciever_addr,
        amt=amount,
        index=asset,
    )
    signed_txn = txn.sign(mnemonic.to_private_key(wallet.mnemonic))
    txn_id = algod_client.send_transaction(signed_txn)

    wait_for_transaction_confirmation(algod_client, txn_id)
    logger.info(
        f"Refunded approval deposit of {amount} from {decho_wallet_addr} to {reciever_addr}!"
    )
