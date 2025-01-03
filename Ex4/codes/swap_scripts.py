from bitcoin.core.script import *

######################################################################
# This function will be used by Alice and Bob to send their respective
# coins to a utxo that is redeemable either of two cases:
# 1) Recipient provides x such that hash(x) = hash of secret 
#    and recipient signs the transaction.
# 2) Sender and recipient both sign transaction
# 
# TODO: Fill this in to create a script that is redeemable by both
#       of the above conditions.
# 
# See this page for opcode: https://en.bitcoin.it/wiki/Script
#
#

# This is the ScriptPubKey for the swap transaction
def coinExchangeScript(public_key_sender, public_key_recipient, hash_of_secret):
    return [
        public_key_recipient,
        OP_CHECKSIG,
        OP_IF,
            OP_IF,
                #OP_DUP,
                OP_HASH160,
                hash_of_secret,
                OP_EQUAL,
                OP_IF,
                    OP_1,
                OP_ENDIF,
            OP_ELSE,
                public_key_sender,
                OP_CHECKSIG,
                OP_IF,
                    OP_1,
                OP_ENDIF,
            OP_ENDIF,
        OP_ENDIF

    ]

# This is the ScriptSig that the receiver will use to redeem coins
def coinExchangeScriptSig1(sig_recipient, secret):
    return [
        sig_recipient,
        secret
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed
def coinExchangeScriptSig2(sig_sender, sig_recipient):
    return [
        sig_recipient,
        sig_sender
    ]

#
#
######################################################################

