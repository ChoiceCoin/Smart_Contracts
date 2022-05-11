
import random as r
from algosdk import account, encoding, mnemonic,transaction
from algosdk.future.transaction import AssetTransferTxn, PaymentTxn
from algosdk.v2client import algod

#This is an Algogenous Smart Contract for a guessing game where if  the user wins he/she gets a reward of a particular amount of a token of your choice and if the player loses he/she loses that same amount of a token of your choice 
#Connect to the Algorand Client (This is for sandbox) here. 
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

#Initializes Client for node
headers = {"X-API-Key": algod_token }
algod_client = algod.AlgodClient(algod_token,algod_address,headers)


#The fund address and fund mnemonic defined below should belong to the creator account that controls the asset that you want to offer.

#In this code I created an ASA TEE COIN on the testnet which I used to reward the user, but you can decide to change it up and use your own asa with a diffrent address and passphrase

#The address I used is  KE3P22YHKMC23OHDPYIMGVG7DHA6GP6T6DBROYRTZX3RQJ73Y2EFM5OEO4
#The passphrase  is : light truck alley era debris mango country lake solution impact captain casual steel mechanic coil ceiling exhibit reject skirt february apart parent master able random
#Warning !!!! This is solely for development purposes and the tokens have 0 value.

creator_address = "KE3P22YHKMC23OHDPYIMGVG7DHA6GP6T6DBROYRTZX3RQJ73Y2EFM5OEO4" #Put the creator address here. 
creator_mnemonic = "light truck alley era debris mango country lake solution impact captain casual steel mechanic coil ceiling exhibit reject skirt february apart parent master able random" #Put the creator mnemonic here. 
fund_key = mnemonic.to_private_key(creator_mnemonic)

#Asset ID for Tee Coin
asset_id = "88713385"

#Welocome Screen
#This prompts the user to input his/her name,testnet address with sufficent algos and the required asa, and their passpharase
print("WELCOME TO THE PRICE IS RIGHT \nGUESS THE RIGHT NUMBER AND GET A CHANCE TO WIN ANY AMOUNT TEECOIN\n---------DISCLAIMER---------\nYOU CAN ALSO LOSE THAT AMOUNT OF TEECOIN IF YOU DONT GUESS RIGHT.")
user_name = input('Type your name : ').title()
print(f'Hello {user_name}.')
user_said = input(f'{user_name} do you want to play Number Guessing game (Y/N) : ').lower()

while True:
    try: 
        user_wage =int(input("ENTER THE AMOUNT OF TEECOIN YOU WANT TO WAGER: "))

    

    except ValueError:
        print("THIS IS NOT A NUMBER")
        continue
    else:
        break
        

user_address = input("\n ENTER YOUR TESTNET ADDRESS WITH SUFFICIENT TESTNET ALGOS: ")
user_key = input("\n PASTE YOUR PASSPHRASE IN THE CORRECT SYNTAX: ")
reciver_address = user_address
reciver_mnemonic = user_key
reciver_key = mnemonic.to_private_key(reciver_mnemonic)
amount = int(user_wage) * 100 
amount2 = amount / 100 
index = asset_id






#This defines a stateless transfer of funds from the creator account  to the user account.  
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

#This defines a stateless transfer of funds from the  user account to the creator account. 
def asset_transfer_user(reciver_address, reciver_key, creator_address, amount, index = asset_id):
    parameters = algod_client.suggested_params()
    transaction = AssetTransferTxn(reciver_address, parameters, creator_address, amount, index =  asset_id )
    signature = transaction.sign(reciver_key)
    #Signs the transaction with the senders private key
    algod_client.send_transaction(signature)
    #Sends the transaction with the signature
    final = transaction.get_txid()
    print("TRANSACTION ID : ",final)
    return True, final

#This automates the optin action so the user can recieve the token
def optin(reciver_mnemonic,reciver_address,amount,index):
    parameters = algod_client.suggested_params()
    transaction = AssetTransferTxn(reciver_address, parameters, reciver_address, 0, index = asset_id)
    key = mnemonic.to_private_key(reciver_mnemonic)
    signature = transaction.sign(key)
    algod_client.send_transaction(signature)
    #Opts-in the account to the asset
    return True




#This defines the game logic
def Main(user_said):

    while True:
        

        if ('y' not in user_said) and ('n' not in user_said) and (user_said != True):
            user_said = input('Invalid keyword\nType again : ').lower()

        elif 'y' in user_said:
            winning_number = r.randint(1,100)
            user_guessed = int(input('\nYou have 6 guesses.\nGuess any number between 1 and 100\nGuess the number : '))
            turn = 1

            while True:
            
                if winning_number == user_guessed:
                    print(f'Congrats you guessed the number in {turn} times.')
                    
                    return 1
                    

                elif turn == 6:
                    print(f'Sorry You can\'t guess the number. The number is {winning_number}.')
                    return 0
                   

                else:
                    if winning_number > user_guessed:
                        print('Too Low')
                    else:
                        print('Too High')

                    print(f'You have {6-turn} guesses left.')
                    
                    turn += 1
                    user_guessed = int(input('Guess again : '))

        

#This checks if the user wins or loses and calls the respective functions to carry out the appropriate transaction which prints out the transaction id which can be verified on algoexplorer.
if Main(user_said) == 1:
    print("YOU WON" ,amount2, " TeeCoin" )
    optin(reciver_mnemonic,reciver_address,amount,index)
    asset_transfer_fund(creator_address, fund_key, reciver_address,amount, index = asset_id)
else :
    print("YOU LOST",amount2, " TeeCoin" )
    optin(reciver_mnemonic,reciver_address,amount,index)
    asset_transfer_user(reciver_address, reciver_key, creator_address, amount, index = asset_id)
