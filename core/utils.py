import secrets

from django.conf import settings

algod_client = settings.ALGOD_CLIENT
indexer_client = settings.INDEXER_CLIENT


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
    account = indexer_client.account_info(address)
    # if contains_choice_coin(address):address
    choice_balance = 0
    if account.get("account").get("assets"):
        for asset in account["account"]["assets"]:
            if asset["asset-id"] == settings.CHOICE_ID:
                choice_balance = asset["amount"]
                break

    return choice_balance

    # return 'Error not opted in for Choice'


def check_algo_balance(address: str) -> int:
    account = indexer_client.account_info(address)
    return (account["account"]["amount"]/1000000)


def get_transactions(address: str, asa_id: int):
    """Gets all transactions for a particular ASA on an address"""

    txns = indexer_client.search_asset_transactions(
        asset_id=asa_id,
        txn_type="axfer",
        address=address,
        address_role="receiver",
    )
    return txns["transactions"]


def gen_random_photo_url():
    return f"https://avatars.dicebear.com/api/bottts/{secrets.token_hex(10)}.png"
