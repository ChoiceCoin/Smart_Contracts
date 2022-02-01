import json
from algosdk import account, algod, encoding, mnemonic, transaction

# test wallets accounts were created solely for this process

mnemonic1 = "upgrade arctic vanish connect title embody hair tornado bullet cry truck swear catalog rail rigid increase mandate cage frame isolate shadow fun choose able biology"
mnemonic2 = "already six hello want allow vacuum three great city fetch slow protect describe secret digital mansion motion safe pair dog cool salmon brick about waste"
mnemonic3 = "resource name track ivory peace account auto ship pony tape unhappy grief october island novel install toddler glide comfort mechanic differ disagree when above monkey"




private_key_1 = mnemonic.to_private_key(mnemonic1)
account_1 = mnemonic.to_public_key(mnemonic1)

private_key_2 = mnemonic.to_private_key(mnemonic2)
account_2 = mnemonic.to_public_key(mnemonic2)

private_key_3 = mnemonic.to_private_key(mnemonic3)
account_3 = mnemonic.to_public_key(mnemonic3)


def wait_for_confirmation(txid):
   last_round = acl.status().get('lastRound')
   while True:
       txinfo = acl.pending_transaction_info(txid)
       if txinfo.get('round') and txinfo.get('round') > 0:
           print("Transaction {} confirmed in round {}.".format(
               txid, txinfo.get('round')))
           break
       else:
           print("Waiting for confirmation...")
           last_round += 1
           acl.status_after_block(last_round)





algod_address = "https://testnet-algorand.api.purestake.io/ps2"  # enter your algod_address
algod_token = ""    # enter your algod_token

# Initialize an algod client
acl = algod.AlgodClient(algod_token, algod_address, )

# Get network params for transactions.
params = acl.suggested_params()
first = params.get("lastRound")
last = first + 1000
gen = params.get("genesisID")
gh = params.get("genesishashb64")
min_fee = params.get("minFee")

# create a multisig account
version = 1  # multisig version
threshold = 2  # how many signatures are necessary
msig = transaction.Multisig(version, threshold, [account_1, account_2])
print("Multisig Address: ", msig.address())
input("Please go to: https://bank.testnet.algorand.network/ to fund your multisig account." + '\n' + "Press Enter to continue...")

# get suggested parameters
params = acl.suggested_params()
gen = params["genesisID"]
gh = params["genesishashb64"]
last_round = params["lastRound"]
fee = params["fee"]

# create a transaction
sender = msig.address()
recipient = account_3
amount = 10000
txn = transaction.PaymentTxn(sender, fee, last_round, last_round+100, gh, recipient, amount)

# create a SignedTransaction object
mtx = transaction.MultisigTransaction(txn, msig)

# sign the transaction
mtx.sign(private_key_1)
mtx.sign(private_key_2)

# print encoded transaction
print(encoding.msgpack_encode(mtx))

# send the transaction
transaction_id = acl.send_raw_transaction(encoding.msgpack_encode(mtx))
wait_for_confirmation(transaction_id)
print("\nTransaction was sent!")
print("Transaction ID: " + transaction_id + "\n")