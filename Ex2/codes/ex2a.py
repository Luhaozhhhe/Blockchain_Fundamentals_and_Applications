from sys import exit
from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret
from utils import *
from config import my_private_key, my_public_key, my_address, faucet_address
from ex1 import send_from_P2PKH_transaction


cust1_private_key = CBitcoinSecret(
    'cVDkvR5cVoGWiTtJfiVuTg3zCJWyzUTuoHWdtyFzb2UmCznrP5hu')
cust1_public_key = cust1_private_key.pub
cust2_private_key = CBitcoinSecret(
    'cUTjPkbehgpnRnDHj7saxW1htRWBwB4FnGPw8F1wDF3ARLcPYiEX')
cust2_public_key = cust2_private_key.pub
cust3_private_key = CBitcoinSecret(
    'cSCa4Ddws1DkXfKcN8KFx5n44dQcRZoU318Nk23x9CDjxssLUcUT')
cust3_public_key = cust3_private_key.pub


required_signatures = 3
public_key=[
    cust1_public_key,
    cust2_public_key,
    cust3_public_key
]

ex2a_txout_scriptPubKey = CScript([required_signatures] + public_key + [len(public_key), OP_CHECKMULTISIG])


if __name__ == '__main__':

    amount_to_send = 0.00001
    txid_to_spend = (
        'b95bbc0006084b3edb5d87f55bd05b3696c5d34ca7f7ba74426219d5ebe24615')
    utxo_index = 0


    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        ex2a_txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)
