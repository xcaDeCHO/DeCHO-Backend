import secrets
from algosdk.error import IndexerHTTPError
from algosdk.encoding import is_valid_address
from algosdk.error import IndexerHTTPError
from django.conf import settings


algod_client = settings.ALGOD_CLIENT
indexer_client = settings.INDEXER_CLIENT
fernet = settings.FERNET


def contains_choice_coin(address: str) -> bool:
    """Checks if the address is opt into Choice Coin."""
    account = indexer_client.account_info(address)
    contains_choice = False

    if account.get("account").get("assets"):
        for asset in account["account"]["assets"]:
            if asset["asset-id"] == settings.CHOICE_ID:
                contains_choice = True
                break
    return contains_choice


def check_choice_balance(address: str):
    """Checks if the address is opt into Choice Coin."""
    try:
        account = indexer_client.account_info(address)
        choice_balance = 0
        if account.get("account").get("assets"):
            for asset in account["account"]["assets"]:
                if asset["asset-id"] == settings.CHOICE_ID:
                    choice_balance = int(asset["amount"]) / 100
                    break
        return choice_balance
    except IndexerHTTPError as err:
        print(err)
        return 0


def check_algo_balance(address: str) -> int:
    try:
        account = indexer_client.account_info(address)
        return account["account"]["amount"] / 1000000
    except IndexerHTTPError as err:
        print(err)
        return 0


def get_transactions(address: str, asa_id: int):
    """Gets all transactions for a particular ASA on an address"""
    # This function was written to be used for Cause approval addresses
    try:
        txns = indexer_client.search_asset_transactions(
            asset_id=asa_id,
            txn_type="axfer",
            address=address,
            address_role="receiver",
        )
        return txns["transactions"]

    except IndexerHTTPError:
        return []


def get_algo_sent(address: str):
    """Getting the algo transactions sent by an address """
    transactions = indexer_client.search_transactions(address=address, address_role="sender", txn_type="pay")
    return transactions.get("transactions")


def gen_random_photo_url():
    return f"https://avatars.dicebear.com/api/bottts/{secrets.token_hex(10)}.png"


def decrypt_mnemonic(mnemonic: str) -> str:
    return fernet.decrypt(mnemonic.encode()).decode()


def filter_transactions(from_address: str, to_address, asa_id: int = None):
    if asa_id:
        transactions = get_transactions(address=to_address, asa_id=asa_id)
        required_transactions = []
        for transaction in transactions:
            if transaction.get("sender") == from_address:
                required_transactions.append(transaction)
    else:
        transactions = get_algo_sent(from_address)
        required_transactions = []
        for transaction in transactions:
            if transaction.get("payment-transaction").get("receiver") == to_address:
                required_transactions.append(transaction)

    return required_transactions


def get_algo_transactions(address: str):
    txns = indexer_client.search_transactions(address=address,
                                              address_role="receiver",
                                              txn_type="pay")
    return txns["transactions"]


