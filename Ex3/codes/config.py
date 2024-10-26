from bitcoin import SelectParams
from bitcoin.base58 import decode
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress


SelectParams('testnet')

# TODO: Fill this in with your private key.
#将预备实验中的创建的私钥(private key)写入
my_private_key = CBitcoinSecret(
    'cW3fxHAhp5RRfDcFkbctRPymyYJZe3AEF7UngN8qfnKhkPnccKNj')

my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)

#the teacher SuMing's address
faucet_address = CBitcoinAddress('mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB')
