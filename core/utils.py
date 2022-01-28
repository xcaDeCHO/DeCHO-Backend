# from algosdk.v2client import algod
# from decouple import config
#
# choice_id = config("CHOICE_ID")
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
