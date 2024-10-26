from sys import exit
from bitcoin.core.script import *

from utils import *
from config import my_private_key, my_public_key, my_address, faucet_address
from ex1 import send_from_P2PKH_transaction

ex3a_txout_scriptPubKey = [
    OP_2DUP,
    OP_ADD,
    2211,
    OP_EQUALVERIFY,
    OP_SUB,
    43,
    OP_EQUAL
]

if __name__ == '__main__':
    amount_to_send = 0.00001
    txid_to_spend = (
        'b95bbc0006084b3edb5d87f55bd05b3696c5d34ca7f7ba74426219d5ebe24615')
    utxo_index = 1

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        ex3a_txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)
