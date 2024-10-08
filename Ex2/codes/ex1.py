from bitcoin.core.script import *

from utils import *
from config import (my_private_key, my_public_key, my_address,
                    faucet_address)


def P2PKH_scriptPubKey(address):
    
    script_address=address.to_scriptPubKey()   #script_address基于给定的bitcoin地址生成了一个脚本
    
    temp_hash_value=script_address[3:-2]   #提取出公钥哈希的值
    
    Script_PubKey = [
        OP_DUP,                   # 复制堆栈顶端数据
        OP_HASH160,               # 计算hash函数两次，第一次用SHA-256，第二次用RIPEMD-160
        temp_hash_value,          # 前面计算出来的公钥hash值
        OP_EQUALVERIFY,           # 检查栈顶两个元素是否相等，是一个bool值
        OP_CHECKSIG               # 检查栈顶元素是否是有效签名
    ]

    return Script_PubKey



def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    #创建新的签名
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             my_private_key)
    Public_Key=my_public_key   #获取我们的公钥

    return [signature,Public_Key]   #返回我们的新的签名和公钥



def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':

    #交易的费用，设置的小一点
    amount_to_send = 0.00001

    #split_output.txt中的prev_hash的值
    txid_to_spend = (
        '6a1c1c4257890d699b47685053744bf0db805bd19e96f3d4930bba74de89ec1d')
    
    #utxo索引，依旧是0，因为没有产生过交易
    utxo_index = 0

    txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)
    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)
