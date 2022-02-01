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
choice_id = None

def check__choice_balance(wallet_address):
    response = requests.get(f'{algo_explorer_address}/v2/account/{wallet_address}')
    print(response.json())
    if response.status_code == 200:
        response_dict = response.json()
        for asset in response_dict.get('assets'):
            if asset.get('asset-id') == choice_id:
                return {'status': status.HTTP_200_OK, 'data': asset.get('amount')}
            else:
                return {'status': status.HTTP_412_PRECONDITION_FAILED, 'data': 'Wallet in not opted in for CHOICE. '
                                                                               'Contact a moderator'}

    else:
        return {'status': response.status_code, 'data': response.json()}
