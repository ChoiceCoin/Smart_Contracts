# This is a stateless smart contract that enables participants to send Choice Coin to others.
# The user has to enter their algorand address, mnemonic, the receiver's address, the reason for the payment, and the amount of Choice.
def choice_transaction(receiver,sender_mnemonic,sender_address,amount,comment):
    parameters = algod_client.suggested_params()
    error = ''
    amount = int(amount)
    if encoding.is_valid_address(receiver) and encoding.is_valid_address(sender_address):
        sender_key = mnemonic.to_private_key(sender_mnemonic)
        amount = amount * 100
        final = choice_trade(sender_address,sender_key,receiver,amount,asset_id,comment)
        error = 'Congratulations! The transfer was successful. You can view your transaction details at https://testnet.algoexplorer.io/tx/' + final[1] + "."
    else:
        error = 'Wrong Formatting for Algorand Address'
    return error

# This is a stateful function that records a charge to another account on the Algorand Blockchain.
# It allows users to request funds from another user, much like a payment app. 
# The user has to enter their algorand address, mnemonic, the address of the individual they are charging, and a comment including the reason and the amount being charged.
def request_funds(receiver,sender_mnemonic,sender_address,init_comment):
    parameters = algod_client.suggested_params()
    error = ''
    if encoding.is_valid_address(receiver) and encoding.is_valid_address(sender_address):
        sender_key = mnemonic.to_private_key(sender_mnemonic)
        comment = "This is a Choice Coin charge for " + init_comment + "."
        choice_trade(sender_address,sender_key,receiver,1,asset_id,comment)
    else:
        error = 'Wrong Formatting for Algorand Address'
    return error
