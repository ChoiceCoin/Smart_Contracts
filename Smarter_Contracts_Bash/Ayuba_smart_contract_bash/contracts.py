from pyteal import *
from algosdk import mnemonic,transaction
from algosdk.v2client import algod

reciever_addr = "GNJNOBHDTIH5CM2YKYXAFYMGAGQPDEPILXKQKUBRBAKLJQZB5KEAWJZOGI" #test address for recieving

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "" #put your api key

headers = {"X-API-Key": algod_token }
algod_client = algod.AlgodClient(algod_token,algod_address,headers)

sender_address = "PZGEMXKKSP7NZARBIVO7P3YHI22ROOHMLIEQ2YQDRSMD5ZX7KPT3N76U3E"
sender_mnemonic = "audit child million gloom basic velvet bacon flower address awkward stick oven offer dry tackle whip case kiwi inch lake asthma long screen abstract lock" 
sender_key = mnemonic.to_private_key(sender_mnemonic)

params = algod_client.suggested_params()


#algogeneous smart contract to take an action following an AI input
def create_roles():
    receiver_addr = input("enter your wallet address\n")

    print("please select your role by chosing 0 or 1")
    roles = int(input("0 - Developer\n1 - not a developer\n "))
    init_role = int(roles)
    return init_role,receiver_addr

def algogeneous():
    alg_role1,alg_role2 = create_roles()
    print(alg_role1,alg_role2)
    
    if  alg_role1 > 0:
        print('you are not a dev')
    elif alg_role1 == 0:
        txn = transaction.PaymentTxn(sender_address,1000,params.first,params.last,params.gh,alg_role2,3000)
        signTxn = txn.sign(sender_key)
        txid = algod_client.send_transaction(signTxn)
        print("Transaction ID: ",txid)
    else:
        clear()
    
algogeneous()

def clear():
    return Approve()
