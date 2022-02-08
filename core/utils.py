import requests
from rest_framework import status
from django.conf import settings




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
choice_id = settings.CHOICE_ID


def check__choice_balance(wallet_address):
    try:
        response = requests.get(f'{algo_explorer_address}/v2/accounts/{wallet_address}')
    except Exception as e:
        print('broke')
        print(e)
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


def transactions_list(address):
    try:
        response = requests.get(f'{algo_explorer_address}/v2/accounts/{address}/transactions?asset-id=21364625')
        print(response.json())
        return response.json()
    except Exception as e:
        print('broke')
        print(e)



dict = {
  "current-round": 19623745,
  "next-token": "JlUOAQAAAAAEAAAA",
  "transactions": [
    {
      "asset-transfer-transaction": {
        "amount": 200,
        "asset-id": 21364625,
        "close-amount": 0,
        "receiver": "XAQP4RP2XG47VIZ7HM32MVOPQADXPRJYIQGB3RTMBPFS725TWRLAQXUURM"
      },
      "close-rewards": 0,
      "closing-amount": 0,
      "confirmed-round": 18806271,
      "fee": 258000,
      "first-valid": 18806263,
      "genesis-hash": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
      "genesis-id": "testnet-v1.0",
      "id": "HMJRRQWXORLUFKWCOABCBEXYMZQHN4N6SYJIVJM45YHZSYV74ZKA",
      "intra-round-offset": 9,
      "last-valid": 18807263,
      "receiver-rewards": 0,
      "round-time": 1640779906,
      "sender": "NKZA5FMOLRTYPBH2ESM4YSWP3Y5SJDY4OW6ZNJBENS4AESJSO7MW6TBL64",
      "sender-rewards": 0,
      "signature": {
        "sig": "cgzFXhgpGouzVjP8m3AX7Gyxh5cw+fWaFZGCsODMH+cIxWgDfWUDRxq2R1wbZ4tjNxMWesQRoJw6fk4sotHYDw=="
      },
      "tx-type": "axfer"
    },
    {
      "asset-transfer-transaction": {
        "amount": 200,
        "asset-id": 21364625,
        "close-amount": 0,
        "receiver": "XAQP4RP2XG47VIZ7HM32MVOPQADXPRJYIQGB3RTMBPFS725TWRLAQXUURM"
      },
      "close-rewards": 0,
      "closing-amount": 0,
      "confirmed-round": 18806192,
      "fee": 258000,
      "first-valid": 18806184,
      "genesis-hash": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
      "genesis-id": "testnet-v1.0",
      "id": "QTJWQ4WHRXMPCPCTV7DIGVS6JEDJHW4XZTDCT5JEJFRMEMIEJTEA",
      "intra-round-offset": 9,
      "last-valid": 18807184,
      "receiver-rewards": 0,
      "round-time": 1640779572,
      "sender": "NKZA5FMOLRTYPBH2ESM4YSWP3Y5SJDY4OW6ZNJBENS4AESJSO7MW6TBL64",
      "sender-rewards": 0,
      "signature": {
        "sig": "PEa+sffnL6iAGlNm8Sr4gwrveSpw1JUXzkME9YDuWkvna7JMVK7To4VV2/WP3kseBuvpJutfa08S/nM/5C97CA=="
      },
      "tx-type": "axfer"
    },
    {
      "asset-transfer-transaction": {
        "amount": 5,
        "asset-id": 21364625,
        "close-amount": 0,
        "receiver": "NKZA5FMOLRTYPBH2ESM4YSWP3Y5SJDY4OW6ZNJBENS4AESJSO7MW6TBL64"
      },
      "close-rewards": 0,
      "closing-amount": 0,
      "confirmed-round": 17716667,
      "fee": 1000,
      "first-valid": 17716539,
      "genesis-hash": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
      "genesis-id": "testnet-v1.0",
      "group": "w0bNtU34T4w4UevgFKTDRr/5xhBLAbZJA4hK/oogZDw=",
      "id": "DRDLJQMUNDJJZ7UPNDAZDWPCHMVYOW5RU4PUKZYXPUPOVZTKHM5A",
      "intra-round-offset": 3,
      "last-valid": 17717539,
      "receiver-rewards": 0,
      "round-time": 1636159082,
      "sender": "KGIWAMCB6C5B2VSVSJQAIHCMGLN6LBBKLUW5PBQ5ZNJ2O5CCMQP2YSPLXM",
      "sender-rewards": 0,
      "signature": {
        "logicsig": {
          "args": [],
          "logic": "BCAIAQAAAwSR/5cKBQYhBSQNRDEJMgMSRDEVMgMSRDEgMgMSRDIEIg1EMwEAMQASRDMBECEHEkQzARiB2ZilChJEMwEZIhIzARslEhA3ARoAgAlib290c3RyYXASEEAAXDMBGSMSRDMBG4ECEjcBGgCABHN3YXASEEACEzMBGyISRDcBGgCABG1pbnQSQAE5NwEaAIAEYnVybhJAAYM3ARoAgAZyZWRlZW0SQAIzNwEaAIAEZmVlcxJAAlAAIQYhBCQjEk0yBBJENwEaARchBRI3ARoCFyQSEEQzAgAxABJEMwIQJRJEMwIhIxJEMwIiIxwSRDMCIyEHEkQzAiQjEkQzAiWAB1RNMVBPT0wSRDMCJlEADYANVGlueW1hbiBQb29sIBJEMwIngBNodHRwczovL3RpbnltYW4ub3JnEkQzAikyAxJEMwIqMgMSRDMCKzIDEkQzAiwyAxJEMwMAMQASRDMDECEEEkQzAxEhBRJEMwMUMQASRDMDEiMSRCQjE0AAEDMBATMCAQgzAwEINQFCAYkzBAAxABJEMwQQIQQSRDMEESQSRDMEFDEAEkQzBBIjEkQzAQEzAgEIMwMBCDMEAQg1AUIBVDIEIQYSRDcBHAExABNENwEcATMEFBJEMwIAMQATRDMCFDEAEkQzAwAzAgASRDMDFDMDBzMDECISTTEAEkQzBAAxABJEMwQUMwIAEkQzAQEzBAEINQFCAPwyBCEGEkQ3ARwBMQATRDcBHAEzAhQSRDMDFDMDBzMDECISTTcBHAESRDMCADEAEkQzAhQzBAASRDMDADEAEkQzAxQzAwczAxAiEk0zBAASRDMEADEAE0QzBBQxABJEMwEBMwIBCDMDAQg1AUIAjjIEIQQSRDcBHAExABNEMwIANwEcARJEMwIAMQATRDMDADEAEkQzAhQzAgczAhAiEk0xABJEMwMUMwMHMwMQIhJNMwIAEkQzAQEzAwEINQFCADwyBCUSRDcBHAExABNEMwIUMwIHMwIQIhJNNwEcARJEMwEBMwIBCDUBQgARMgQlEkQzAQEzAgEINQFCAAAzAAAxABNEMwAHMQASRDMACDQBD0M="
        }
      },
      "tx-type": "axfer"
    },
    {
      "asset-transfer-transaction": {
        "amount": 1036,
        "asset-id": 21364625,
        "close-amount": 0,
        "receiver": "NKZA5FMOLRTYPBH2ESM4YSWP3Y5SJDY4OW6ZNJBENS4AESJSO7MW6TBL64"
      },
      "close-rewards": 0,
      "closing-amount": 0,
      "confirmed-round": 17716539,
      "fee": 1000,
      "first-valid": 17716520,
      "genesis-hash": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
      "genesis-id": "testnet-v1.0",
      "group": "9WCgNYW7HCdBYGiirGlMZTPXLQEDLnjenzTR0qElHgs=",
      "id": "CY5PNZ6JGMP7DNJBVKVUUOLV5ATORTMTBGPSOFTEN26M7JP646VQ",
      "intra-round-offset": 6,
      "last-valid": 17717520,
      "receiver-rewards": 0,
      "round-time": 1636158539,
      "sender": "KGIWAMCB6C5B2VSVSJQAIHCMGLN6LBBKLUW5PBQ5ZNJ2O5CCMQP2YSPLXM",
      "sender-rewards": 0,
      "signature": {
        "logicsig": {
          "args": [],
          "logic": "BCAIAQAAAwSR/5cKBQYhBSQNRDEJMgMSRDEVMgMSRDEgMgMSRDIEIg1EMwEAMQASRDMBECEHEkQzARiB2ZilChJEMwEZIhIzARslEhA3ARoAgAlib290c3RyYXASEEAAXDMBGSMSRDMBG4ECEjcBGgCABHN3YXASEEACEzMBGyISRDcBGgCABG1pbnQSQAE5NwEaAIAEYnVybhJAAYM3ARoAgAZyZWRlZW0SQAIzNwEaAIAEZmVlcxJAAlAAIQYhBCQjEk0yBBJENwEaARchBRI3ARoCFyQSEEQzAgAxABJEMwIQJRJEMwIhIxJEMwIiIxwSRDMCIyEHEkQzAiQjEkQzAiWAB1RNMVBPT0wSRDMCJlEADYANVGlueW1hbiBQb29sIBJEMwIngBNodHRwczovL3RpbnltYW4ub3JnEkQzAikyAxJEMwIqMgMSRDMCKzIDEkQzAiwyAxJEMwMAMQASRDMDECEEEkQzAxEhBRJEMwMUMQASRDMDEiMSRCQjE0AAEDMBATMCAQgzAwEINQFCAYkzBAAxABJEMwQQIQQSRDMEESQSRDMEFDEAEkQzBBIjEkQzAQEzAgEIMwMBCDMEAQg1AUIBVDIEIQYSRDcBHAExABNENwEcATMEFBJEMwIAMQATRDMCFDEAEkQzAwAzAgASRDMDFDMDBzMDECISTTEAEkQzBAAxABJEMwQUMwIAEkQzAQEzBAEINQFCAPwyBCEGEkQ3ARwBMQATRDcBHAEzAhQSRDMDFDMDBzMDECISTTcBHAESRDMCADEAEkQzAhQzBAASRDMDADEAEkQzAxQzAwczAxAiEk0zBAASRDMEADEAE0QzBBQxABJEMwEBMwIBCDMDAQg1AUIAjjIEIQQSRDcBHAExABNEMwIANwEcARJEMwIAMQATRDMDADEAEkQzAhQzAgczAhAiEk0xABJEMwMUMwMHMwMQIhJNMwIAEkQzAQEzAwEINQFCADwyBCUSRDcBHAExABNEMwIUMwIHMwIQIhJNNwEcARJEMwEBMwIBCDUBQgARMgQlEkQzAQEzAgEINQFCAAAzAAAxABNEMwAHMQASRDMACDQBD0M="
        }
      },
      "tx-type": "axfer"
    },
    {
      "asset-transfer-transaction": {
        "amount": 0,
        "asset-id": 21364625,
        "close-amount": 0,
        "receiver": "NKZA5FMOLRTYPBH2ESM4YSWP3Y5SJDY4OW6ZNJBENS4AESJSO7MW6TBL64"
      },
      "close-rewards": 0,
      "closing-amount": 0,
      "confirmed-round": 17716518,
      "fee": 1000,
      "first-valid": 17716458,
      "genesis-hash": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
      "genesis-id": "testnet-v1.0",
      "id": "NC3OQQ33FP3VGZ4KRVFMF6STXQTCQ3CQTZ3MH6WVG7GAHVVQFWGA",
      "intra-round-offset": 4,
      "last-valid": 17717458,
      "receiver-rewards": 0,
      "round-time": 1636158450,
      "sender": "NKZA5FMOLRTYPBH2ESM4YSWP3Y5SJDY4OW6ZNJBENS4AESJSO7MW6TBL64",
      "sender-rewards": 0,
      "signature": {
        "sig": "7CNNRPJjqHbJSs3n88+P+aAKDsonwUIHAZs72wp3taEP4hkfoYn3jXhT4gf+lzAOMBzUSI0ZohqrKHyip+PnAw=="
      },
      "tx-type": "axfer"
    }
  ]
}