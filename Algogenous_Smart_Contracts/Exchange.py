#Copyright Fortior Blockchain 2021.
from algosdk import account, encoding, mnemonic,transaction
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn
from algosdk.v2client import algod

#This defines an Algogenous Smart Contract for running an exchnage between an asset such as Choice Coin
#and other Algorand-Standard-Assets. You can use this smart contract to offer any Algorand Standard Assets
#for exchange to a small community. The Algogenous Smart Contract Integrates an embedded intelligence to
#automatically create a legal contract on the Algorand Blockchain certifying an exchnage took place.
#It records the name of the individual who purchased the asset plus the signature of a representative of 
#the organization selling the main asset. The legal contract can be found under the "notes" section 
#of a transaction in the Algorand Mobile Wallet.

#Connect to the Algorand Client here. This code was tested using the PureStake API.
algod_address = ""
algod_token = ""
#Initializes Client for node
headers = {"X-API-Key": algod_token }
algod_client = algod.AlgodClient(algod_token,algod_address,headers)
#The fund address and fund mnemonic defined below should belong to the manager account that controls the 
#asset that you want to offer.
fund_address = "" #Put the main manager address here. This is an address that you should retain control over.
fund_mnemonic = "" #Put the main_manager_mnemonic here. Again, this is should be an account you retain control over.
fund_key = mnemonic.to_private_key(fund_mnemonic)
asset_id = 17264161 #This is the Choice Coin Test Asset ID. Change this to the asset id of an asset with a manager address that you control.

asset_2_id = 16538896 #This is a random testnet ID of an asset we control. Change this to the asset id of the asset that you 
#want individuals to trade with for your asset.






#This defines a stateless smart contract to transfer Algo from one account to another.

def algo_trade(sender, key, receiver, amount,comment):
    parameters = algod_client.suggested_params()
    #Initalize parameters
    transaction = PaymentTxn(sender, parameters, receiver, amount,note=comment)
    #Defines an inital transaction for Algo.
    signature = transaction.sign(key)
    #Signs the transaction with the sender's private key
    algod_client.send_transaction(signature)
    #Sends the transaction with the signature
    return True

  
  
  
  
  
#This defines another stateless transaction that sends an asset from one account to another.  
  
def asset_trade(sender, key, receiver, amount, index,comment):
    parameters = algod_client.suggested_params()
    transaction = AssetTransferTxn(sender, parameters, receiver, amount, index,note=comment)
    #Defines an inital transaction for Asset Coin
    signature = transaction.sign(key)
    #Signs the transaction with the senders private key
    algod_client.send_transaction(signature)
    #Sends the transaction with the signature
    final = transaction.get_txid()
    return True, final

  
  
  
  
  #This defines an opt-in function for an asset. It automates the optin process for
  #user accounts who may be purschasing an asset.
def create_optin(receiver_mnemonic,receiver_address,amount,index):
    parameters = algod_client.suggested_params()
    transaction = AssetTransferTxn(receiver_address, parameters, receiver_address, 0, index)
    #Defines a transaction that will opt the receiver into the asset.
    key = mnemonic.to_private_key(receiver_mnemonic)
    signature = transaction.sign(key)
    algod_client.send_transaction(signature)
    #Opts-in the account to the asset
    return True

  
  
#This is an Algogenous Smart Contract. It first checks to ensure that 
#all the inputs have been filled correctly. Next, it uses the functions 
#defined previously to create an on-chain swap between Algorand and the 
#main standard asset. Finally, it used an embedded intelligence to create a legal contract
#on the Algorand Blockchain. 
def main_exchange_algo(address, receiver_mnemonic,amount,name):
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
            comment = "This is a legal contract between " + init_comment + " and Fortior Blockchain. " + init_comment + " will send " + algo_num + "00 Algos in exchange for " + Asset_num + ".00 Asset. \n Fortior Blockchain Signature: /s/ Archie Chaudhury, CEO of Fortior Blockchain \n Participant Signature: /s/"+ init_comment
            algo_trade(address,receiver_key,fund_address,algo_amount,comment)
            final = asset_trade(fund_address, fund_key, address, Asset_amount, asset_id,comment)
            error = 'Congratulations! The exchange was successful. You can view your transaction details at https://testnet.algoexplorer.io/tx/' + final[1] + "."
    else:
        error = "Wrong Algorand Address"
    return error
  
  
  
#This is another Algogenous Smart Contract. It first checks to ensure that 
#all the inputs have been filled correctly. Next, it uses the functions 
#defined previously to create an on-chain swap between the 
#main standard asset and a second asset that users can exchange. Finally, it used an embedded intelligence to create a legal contract
#on the Algorand Blockchain. 
  def main_exchange_asset(address, receiver_mnemonic,amount,name):
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
            asset_amount = amount * 100
            asset_2_amount = amount * 100 #Define a new exchange rate based on perceived market value. This assumes a one-to-one exchange ratio.
            asset_num = str(amount)
            comment = "This is a legal contract between " + init_comment + " and [your organization name. " + init_comment + " will send " + asset_name + "00 [Asset2] in exchange for " + asset_num + ".00 Asset. \n [Organization Name] Signature: /s/ [Representative Name] \n Participant Signature: /s/"+ name
            asset_trade(address,receiver_key,fund_address,asset_2_amount, asset_2_id,comment)
            final = asset_trade(fund_address, fund_key, address, asset_amount, asset_id,comment)
            error = 'Congratulations! The exchange was successful. You can view your transaction details at https://testnet.algoexplorer.io/tx/' + final[1] + "."
    else:
        error = "Wrong Algorand Address"
    return error
