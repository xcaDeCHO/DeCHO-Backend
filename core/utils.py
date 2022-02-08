from algosdk.v2client.indexer import IndexerClient
from django.conf import settings

CHOICE_ID = settings.CHOICE_ID


def wait_for_transaction_confirmation(algod_client, transaction_id: str):
    """Wait until the transaction is confirmed or rejected, or until timeout snumber of rounds have passed."""

    TIMEOUT = 5
    start_round = algod_client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + TIMEOUT:
        try:
            pending_txn = algod_client.pending_transaction_info(transaction_id)
        except Exception:
            return
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception("pool error: {}".format(pending_txn["pool-error"]))

        algod_client.status_after_block(current_round)
        current_round += 1
    raise Exception("pending tx not found in TIMEOUT rounds, TIMEOUT value = : {}".format(TIMEOUT))


# TODO: You probably want to your opt in error here
def check_choice_balance(algod_client, address):
    """Checks if the address is opt into Choice Coin."""
    account = algod_client.account_info(address)
    choice_balance = 0

    for asset in account["assets"]:
        if asset["asset-id"] == CHOICE_ID:
            choice_balance = asset["amount"]
            break

    return choice_balance


def contains_choice_coin(algod_client, address: str) -> bool:
    """Checks if the address is opt into Choice Coin."""
    account = algod_client.account_info(address)
    contains_choice = False

    for asset in account["assets"]:
        if asset["asset-id"] == CHOICE_ID:
            contains_choice = True
            break

    return contains_choice


def get_transactions(indexer_client: IndexerClient, address: str, asa_id: int):
    """Gets all transactions for a particular ASA on an address"""

    txns = indexer_client.search_asset_transactions(
        asset_id=asa_id,
        txn_type="axfer",
        address=address,
        address_role="receiver",
    )
    return txns["transactions"]
