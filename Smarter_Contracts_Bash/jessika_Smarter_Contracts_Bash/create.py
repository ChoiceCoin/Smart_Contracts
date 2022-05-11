from algosdk import account, mnemonic
#This generates an algorand wallet with an address and the passphrase  
#This can be used on the testnet and the mainnet
def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))


generate_algorand_keypair()
