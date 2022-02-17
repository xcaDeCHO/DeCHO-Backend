import datetime
import logging
import time

from algosdk import mnemonic
from algosdk.future import transaction
from decouple import config
from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task, task

from .models import Cause, Wallet
from .utils import check_algo_balance, check_choice_balance, contains_choice_coin, get_transactions

algod_client = settings.ALGOD_CLIENT
indexer_client = settings.INDEXER_CLIENT

logger = logging.getLogger("huey")


@task()
def test_huey():
    print("This is just a test")


# Two retries might be too much
# @task(retries=2)
def fund_wallet(wallet_address):
    logger.info(f"Funding wallet {wallet_address}...")

    suggested_params = algod_client.suggested_params()
    central_address = config("CENTRAL_WALLET_ADDRESS")
    unsigned_txn = transaction.PaymentTxn(
        central_address, suggested_params, wallet_address, 300000, None, ""
    )
    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(config("CENTRAL_MNEMONIC")))
    txid = algod_client.send_transaction(signed_txn)

    time.sleep(6)
    # transaction.wait_for_confirmation(algod_client, txid)
    logger.info(f"Funded wallet successfully! {wallet_address}")
    print(txid)

    opt_in_to_choice(wallet_address)


def opt_in_to_choice(address):
    logger.info(f"Opting into $CHOICE ASA for {address}...")

    wallet = Wallet.objects.get(address=address)

    suggested_params = algod_client.suggested_params()
    unsigned_transaction = transaction.AssetTransferTxn(
        wallet.address, suggested_params, wallet.address, 0, settings.CHOICE_ID
    )
    signed_transaction = unsigned_transaction.sign(mnemonic.to_private_key(wallet.mnemonic))
    transaction_id = algod_client.send_transaction(signed_transaction)

    time.sleep(5)
    # transaction.wait_for_confirmation(algod_client, transaction_id)

# logger.info(f"Opted into $CHOICE ASA for {address} successful!")


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
            transactions = get_transactions(address, settings.CHOICE_ID)
            for _transaction in transactions:
                refund_from_approval(
                    wallet=cause.decho_wallet,
                    reciever=_transaction.get("sender"),
                    amount=int(_transaction.get("asset-transfer-transaction").get("amount")),
                    asset=settings.CHOICE_ID,
                )
            return
        elif datetime.date.today() > cause.cause_approval.expiry_date:
            cause.status = "canceled"
            transactions = get_transactions(indexer_client, address, settings.CHOICE_ID)
            for _transaction in transactions:
                refund_from_approval(
                    wallet=cause.decho_wallet,
                    reciever=_transaction.get("sender"),
                    amount=int(_transaction.get("asset-transfer-transaction").get("amount")),
                    asset=settings.CHOICE_ID,
                )
            return


@db_periodic_task(crontab("*/30"))
def update_cause_from_approved():
    logger.info("Attempting to update causes status from approval...")

    causes = Cause.objects.filter(status="Approved")
    logger.info(f"Found {causes.count()} causes being donated to!")
    for cause in causes:
        algo_balance = check_algo_balance(address=cause.decho_wallet.address)
        if algo_balance / 100000 >= cause.donations.goal:
            receiver = cause.wallet_address
            sender = cause.decho_wallet
            amount = cause.donations.goal
            transfer_algo(receiver=receiver, sender=sender, amount=amount)
            cause.status = "done"
            cause.save()
        elif datetime.date.today() > cause.donations.expiry_date:
            cause.status = "canceled"
            cause.save()
            transactions = get_transactions(indexer_client, cause.decho_wallet.address)
            for _transaction in transactions:
                if _transaction.get("sender") == cause.decho_wallet.address:
                    pass
                else:
                    transfer_algo(
                        receiver=_transaction.get("sender"),
                        sender=cause.decho_wallet,
                        amount=int(_transaction.get("asset-transfer-transaction").get("amount")),
                    )
            return


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

    time.sleep(4)
    # transaction.wait_for_confirmation(algod_client, txn_id)
    logger.info(
        f"Refunded approval deposit of {amount} from {decho_wallet_addr} to {reciever_addr}!"
    )


@db_task()
def donation_goal_reached_transfer(cause: Cause):
    receiver = cause.wallet_address
    sender = cause.decho_wallet


# @db_task()
# def refund_algo(sender: Wallet, receiver: str):
#     pass


@db_task()
def transfer_algo(receiver, sender, amount):
    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(
        sender=sender.address, sp=params, receiver=receiver, amt=amount
    )
    signed_txn = unsigned_txn.sign(mnemonic.to_private_key(sender.mnemonic))
    txn_id = algod_client.send_transaction(signed_txn)

    time.sleep(4)
    # transaction.wait_for_confirmation(algod_client, txn_id)
    logger.info(f"Sent algo(cause goal reached) {amount} from {sender.address} to {receiver}!")
