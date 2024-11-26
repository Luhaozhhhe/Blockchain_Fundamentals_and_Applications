from bitcoin import SelectParams
from bitcoin.core import CMutableTransaction, x
from bitcoin.core.script import CScript, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH

from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress


from utils import create_txin, create_txout, broadcast_transaction


def split_coins(amount_to_send, txid_to_spend, utxo_index, n, network):
    txin_scriptPubKey = my_address.to_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txout_scriptPubKey = my_address.to_scriptPubKey()
    txout = create_txout(amount_to_send / n, txout_scriptPubKey)
    tx = CMutableTransaction([txin], [txout]*n)
    sighash = SignatureHash(txin_scriptPubKey, tx,
                            0, SIGHASH_ALL)
    txin.scriptSig = CScript([my_private_key.sign(sighash) + bytes([SIGHASH_ALL]),
                              my_public_key])
    VerifyScript(txin.scriptSig, txin_scriptPubKey,
                 tx, 0, (SCRIPT_VERIFY_P2SH,))
    response = broadcast_transaction(tx, network)
    print(response.status_code, response.reason)
    print(response.text)

if __name__ == '__main__':
    SelectParams('testnet')

    ######################################################################
    # TODO: set these parameters correctly
    #
    #hex_key = '06f504114d5bdecf6d67f5a4c9a3d2ef7a55daca4d14f27cded40f4c004ad9c7'
    #my_private_key = CBitcoinSecret.from_secret_bytes(bytes.fromhex(hex_key))
    my_private_key = CBitcoinSecret('cVid8cPTTJNSmS5L8T6EnJSfEgPDu7d8nF1X7HXj5nx4VdDRRgEM')

    my_public_key = my_private_key.pub
    my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)

    amount_to_send = 0.0001 # amount of BTC in the output you're splitting minus fee
    txid_to_spend = (
        '90b30809856029a960aa3ecb9001d7f22dab31b1d9752770e5bf087a442aede5')
    utxo_index = 0
    n = 10 # number of outputs to split the input into
    network = 'btc-test3' # either 'btc-test3' or 'bcy-test'

    #
    #
    ######################################################################

    split_coins(amount_to_send, txid_to_spend, utxo_index, n, network)
