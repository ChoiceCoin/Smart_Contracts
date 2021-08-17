#Copyright Fortior Blockchain 2021.
#Apache License
from algosdk import account, encoding, mnemonic,transaction
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn
from algosdk.v2client import algod

#This defines an Algogenous Smart Contract for running an switch between an asset such as Choice Coin and other ASAs. 
#The Algogenous Smart Contract Integrates an embedded intelligence to automatically create a smart contract on the Algorand Blockchain certifying an switch took place.
#Connect to the Algorand Client here. 
algod_address = ""
algod_token = ""
#Initializes Client for node
headers = {"X-API-Key": algod_token }
algod_client = algod.AlgodClient(algod_token,algod_address,headers)
#The fund address and fund mnemonic defined below should belong to the manager account that controls the asset that you want to offer.
fund_address = "" #Put the main manager address here. 
fund_mnemonic = "" #Put the main_manager_mnemonic here. 
fund_key = mnemonic.to_private_key(fund_mnemonic)
asset_id = ""
asset_2_id = ""

#This defines a stateless smart contract to transfer Algo from one account to another.
def algo_flip(sender, key, receiver, amount,comment):
    parameters = algod_client.suggested_params()
    #Initalize parameters
    transaction = PaymentTxn(sender, parameters, receiver, amount,note=comment)
    #Defines an inital flip for Algo.
    signature = transaction.sign(key)
    #Signs the flip with the sender's private key
    algod_client.send_transaction(signature)
    #Sends the flip with the signature
    return True

#This defines another stateless rotation that sends an asset from one account to another.  
def asset_rotate(sender, key, receiver, amount, index,comment):
    parameters = algod_client.suggested_params()
    transaction = AssetTransferTxn(sender, parameters, receiver, amount, index,note=comment)
    #Defines an inital rotation for Asset Coin
    signature = transaction.sign(key)
    #Signs the rotation with the senders private key
    algod_client.send_transaction(signature)
    #Sends the rotation with the signature
    final = transaction.get_txid()
    return True, final

#This defines an opt-in function for an asset. 
#It automates the optin process for user accounts who may be purschasing an asset.
def create_optin(receiver_mnemonic,receiver_address,amount,index):
    parameters = algod_client.suggested_params()
    transaction = AssetTransferTxn(receiver_address, parameters, receiver_address, 0, index)
    #Defines a transaction that will opt the receiver into the asset.
    key = mnemonic.to_private_key(receiver_mnemonic)
    signature = transaction.sign(key)
    algod_client.send_transaction(signature)
    #Opts-in the account to the asset
    return True

#This is an Algogenous Smart Contract. 
#It first checks to ensure that all the inputs have been filled correctly. 
#Next, it uses the functions defined previously to create an on-chain switch between Algorand and the main standard asset. 
def switch_algo(address, receiver_mnemonic,amount,name):
    parameters = algod_client.suggested_params()
    error = ''
    if encoding.is_valid_address(address):
        if amount == '':
            error = "You did not enter an amount!"
            return error
        elif init_comment == '':
            error = "You did not provide a name for a legal signature!"
            return error
        else:
            amount = int(amount)
            create_optin(receiver_mnemonic, address, 0, asset_id)
            receiver_key = mnemonic.to_private_key(receiver_mnemonic)
            Asset_amount = amount * 100
            algo_amount = amount * 20000
            Asset_num = str(amount)
            algo_num = amount * 0.02
            algo_num = str(algo_num)
            comment = "This is a smart contract between "
            algo_flip(address,receiver_key,fund_address,algo_amount,comment)
            final = asset_rotate(fund_address, fund_key, address, Asset_amount, asset_id,comment)
            error = "Congratulations! The switch was successful."
    else:
        error = "Wrong Algorand Address"
    return error
  
#This is another Algogenous Smart Contract. 
#It first checks to ensure that all the inputs have been filled correctly. 
#Next, it uses the functions defined previously to create an on-chain swap between the main standard asset and a second asset that users can flip.  
  def main_asset_switch(address, receiver_mnemonic,amount,name):
    parameters = algod_client.suggested_params()
    error = ''
    if encoding.is_valid_address(address):
        if amount == '':
            error = "You did not enter an amount!"
            return error
        elif init_comment == '':
            error = "You did not provide a name or signature!"
            return error
        else:
            amount = int(amount)
            create_optin(receiver_mnemonic, address, 0, asset_id)
            receiver_key = mnemonic.to_private_key(receiver_mnemonic)
            asset_amount = amount * 100
            asset_2_amount = amount * 100 
            asset_num = str(amount)
            comment = "This is a smart contract."
            asset_rotate(address,receiver_key,fund_address,asset_2_amount, asset_2_id,comment)
            final = asset_rotate(fund_address, fund_key, address, asset_amount, asset_id,comment)
            error = "Congratulations! The switch was successful."
    else:
        error = "Wrong Algorand Address"
    return error
