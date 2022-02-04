import requests
from rest_framework import status

# from algosdk.v2client import algod
# from decouple import config
#
# testnet_choice_id = config("TESTNET_CHOICE_ID")
# algod_token = config("TOKEN")
#
# algod_address = "https://testnet-algorand.api.purestake.io/ps2"
# headers = {"X-API-Key": algod_token}
# algod_client = algod.AlgodClient(algod_token, algod_address, headers)
#
#
# def contains_choice_coin(asa):
#     account = algod_client.account_info(asa)
#     contains_choice = False
#     for asset in account["assets"]:
#         if asset["asset-id"] == choice_id:
#             contains_choice = True
#             break
#     return contains_choice
#
#
# def check_choice_balance(asa):
#     if contains_choice_coin(asa):
#         for asset in algod_client.account_info(asa)["assets"]:
#             if asset["asset-id"] == choice_id:
#                 return asset["amount"]
#     return "ASA do not contain choice"
#
#
# def view(asa):
#     algo_balance = algod_client.account_info(asa)["amount"]
#     choice_balance = check_choice_balance(asa)
#     return {"algo_balance": algo_balance, "choice_balance": choice_balance}
algo_explorer_address = 'https://algoindexer.testnet.algoexplorerapi.io'
choice_id = 21364625


def check__choice_balance(wallet_address):
    try:
        response = requests.get(f'{algo_explorer_address}/v2/accounts/{wallet_address}')
    except:
        print('broke')
        return 0
    print(response.status_code)
    print(response.json())
    if response.status_code == 200:
        response_dict = response.json()
        try:
            for asset in response_dict.get('account').get('assets'):
                if asset.get('asset-id') == choice_id:
                    return asset.get('amount') / 100
                else:
                    return 'Error: not Opted in'
        except TypeError:
            return 'Error: not Opted in'
    else:
        print(0)
        return 0
