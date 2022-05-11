from algosdk import account, encoding, mnemonic,transaction
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn
from algosdk.v2client import algod

#This is an Algogenous Smart Contract for a guessing game where if  the user wins he/she gets a reward of a particular amount of a token of your choice and if the player loses he/she loses that same amount of a token of your choice 
#Connect to the Algorand Client (This is for sandbox) here. 
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


creator_address = "KE3P22YHKMC23OHDPYIMGVG7DHA6GP6T6DBROYRTZX3RQJ73Y2EFM5OEO4" #Put the creator address here. 
creator_mnemonic = "light truck alley era debris mango country lake solution impact captain casual steel mechanic coil ceiling exhibit reject skirt february apart parent master able random" #Put the creator mnemonic here. 
fund_key = mnemonic.to_private_key(creator_mnemonic)

asset_id = "88713385"

#Initializes Client for node
headers = {"X-API-Key": algod_token }
algod_client = algod.AlgodClient(algod_token,algod_address,headers)

def asset_transfer_fund(creator_address, fund_key, reciver_address,amount, index = asset_id):
    parameters = algod_client.suggested_params()
    transaction = AssetTransferTxn(creator_address, parameters, reciver_address, amount, index =  asset_id )
    signature = transaction.sign(fund_key)
    #Signs the transaction
    algod_client.send_transaction(signature)
    #Sends the transaction with the signature
    final = transaction.get_txid()
    print("TRANSACTION ID : " ,final)
    return True, final
