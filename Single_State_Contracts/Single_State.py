# This is a stateless smart contract that enables participants to send Choice Coin to others.
def choice_flip(receiver,sender_mnemonic,sender_address,amount,comment):
    parameters = algod_client.suggested_params()
    error = ''
    amount = int(amount)
    if encoding.is_valid_address(receiver) and encoding.is_valid_address(sender_address):
        sender_key = mnemonic.to_private_key(sender_mnemonic)
        amount = amount * 100
        final = choice_trade(sender_address,sender_key,receiver,amount,asset_id,comment)
        error = 'Congratulations!"
    else:
        error = 'Wrong Formatting for Algorand Address'
    return error

#This is a stateful smart contract
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