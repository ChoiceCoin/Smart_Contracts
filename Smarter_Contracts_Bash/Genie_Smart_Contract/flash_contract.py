from pyteal import *
import os
import base64
from algosdk.future import transaction
from algosdk import account, mnemonic
from algosdk.v2client import algod


# user declared account mnemonics
creator_mnemonic = ""
# user declared algod connection parameters. Node must have EnableDeveloperAPI set to true in its config
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "" 
headers = {
    "X-API-Key": algod_token,
}

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

def get_private_key_from_mnemonic(mn) :
    private_key = mnemonic.to_private_key(mn)
    return private_key


# helper function that formats global state for printing
def format_state(state):
    formatted = {}
    for item in state:
        key = item['key']
        value = item['value']
        formatted_key = base64.b64decode(key).decode('utf-8')
        if value['type'] == 1:
            # byte string
            if formatted_key == 'voted':
                formatted_value = base64.b64decode(value['bytes']).decode('utf-8')
            else:
                formatted_value = value['bytes']
            formatted[formatted_key] = formatted_value
        else:
            # integer
            formatted[formatted_key] = value['uint']
    return formatted


# helper function to read app global state
def read_global_state(client, app_id):
    app = client.application_info(app_id)
    global_state = app['params']['global-state'] if "global-state" in app['params'] else []
    return format_state(global_state)


def approval_program():

    contract_addr = Global.current_application_address()
    creator = Global.creator_address()
    arg1 = Txn.application_args[0] # noop(no-operation), makes call to the application
    arg2 = Btoi(Txn.application_args[0]) # btoi (converts bytes to uint64)
    staked = App.localGet(Int(0), Bytes("staked"))
    total_staked = App.globalGet(Bytes("total"))
    min_fee = Global.min_txn_fee()

    i = ScratchVar(TealType.uint64) # index used in "for" loop
    num_calls = ScratchVar(TealType.uint64) # number of app calls to this addr found in the gtxns

    # to make sure that the payment comes to this contract
    check_payment = And(
        Gtxn[0].type_enum() == TxnType.Payment,
        Gtxn[0].receiver() == contract_addr,
    )

    # handles creation, initializes contract with 0 staked
    handle_create = Seq(
        App.globalPut(Bytes("total"), Int(0)),
        Approve()
    )

    # makes sure the contract is paid to account for the starting stake, 
    # and sets the local and global variables
    handle_optin = Seq(
        Assert(check_payment),
        App.localPut(Int(0), Bytes("staked"), Gtxn[0].amount()),
        App.globalPut(Bytes("total"), total_staked + Gtxn[0].amount()),
        Approve()
    )

    # sends back all of the staked amount
    handle_closeout = Seq(
        InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: Txn.sender(),
                TxnField.amount: staked - min_fee,
            }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

    # supplies the funds of the loan to the sender of the app call
    send_funds = Seq(
        InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: Txn.sender(),
                TxnField.amount: arg2,
            }),
        InnerTxnBuilder.Submit(),
        Approve()
    )


    # checks if the txn is repaying the loan
    def checkRepay(n):
        return And(
            Gtxn[n].receiver() == contract_addr, 
            Gtxn[n].amount() >= arg2 * Int(101) / Int(100), 
            Gtxn[n].type_enum() == TxnType.Payment
        )

    # checks for more than one borrowing app calls
    def checkDup(n):
        return Seq(
            If(And(Gtxn[n].type_enum() == TxnType.ApplicationCall, Gtxn[n].application_id() == Btoi(contract_addr)),
                If(num_calls.load() == Int(1), 
                    Reject(), 
                    num_calls.store(Int(1))
                )
            ),
            Int(1)
        )

    # when someone wants a flash loan
    handle_loan = Seq(
        num_calls.store(Int(0)),
        # make sure there aren't 2 loan calls
        For(i.store(Int(0)), i.load() < Global.group_size(), i.store(i.load() + Int(1))).Do(
            If(checkDup(i.load()),
                i.store(i.load() + Int(1)),
                Reject())),
        # make sure loan is repayed
        For(i.store(Int(0)), i.load() < Global.group_size(), i.store(i.load() + Int(1))).Do(
            If(checkRepay(i.load()),
                send_funds, # will Approve() if evaluated properly
                i.store(i.load() + Int(1)))),
        Reject()
    )

    # handles when someone wants to increase their amount staked
    handle_fund = Seq(
        Assert(check_payment),
        App.localPut(Int(0), Bytes("staked"), staked + Gtxn[0].amount()),
        App.globalPut(Bytes("total"), total_staked + Gtxn[0].amount()),
        Approve()
    )

    # handles when someone wants to decrease their amount staked
    handle_withdrawal = Seq(
        Assert(arg2 <= staked),
        InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: Txn.sender(),
                TxnField.amount: arg2,
            }),
        InnerTxnBuilder.Submit(),
        App.localPut(Int(0), Bytes("staked"), staked - arg2 - min_fee),
        Approve()
    )

    # handles the redemption of borrowing fees
    handle_redeem = Seq(
        InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: creator,
                TxnField.amount: Balance(contract_addr) - total_staked - MinBalance(contract_addr) - min_fee,
            }),
        InnerTxnBuilder.Submit(),
        Approve()
    )

    handle_noop = Cond(
        [arg1 == Bytes("fund"), handle_fund],
        [arg1 == Bytes("withdraw"), handle_withdrawal],
        [arg1 == Bytes("loan"), handle_loan],
        [arg1 == Bytes("redeem"), handle_redeem]
    )

    program = Cond(
        [Txn.application_id() == Int(0), handle_create],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

    return compileTeal(program, mode=Mode.Application, version=5)

# shouldn't be necessary since there's no opting in, but always approve it
def clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, mode=Mode.Application, version=5)



# create new application
def create_app(client, private_key, approval_program, clear_state_program, global_schema, local_schema):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    # declare handle_create as NoOp
    handle_create = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationCreateTxn(sender, params, handle_create, \
                                            approval_program, clear_state_program, \
                                            global_schema, local_schema)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # wait for confirmation
    try:
        transaction_response = transaction.wait_for_confirmation(client, tx_id, 5)
        print("TXID: ", tx_id)
        print("Result confirmed in round: {}".format(transaction_response['confirmed-round']))

    except Exception as err:
        print(err)
        return

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new app-id:", app_id)

    return app_id


def main() :
    # initialize an algodClient
    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    # define private keys
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)

    # declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    global_ints = 1
    global_bytes = 0
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # compile program to TEAL assembly
    with open("./approval.teal", "w") as f:
        approval_program_teal = approval_program()
        f.write(approval_program_teal)


    # compile program to TEAL assembly
    with open("./clear.teal", "w") as f:
        clear_state_program_teal = clear_state_program()
        f.write(clear_state_program_teal)

    # compile program to binary
    approval_program_compiled = compile_program(algod_client, approval_program_teal)

    # compile program to binary
    clear_state_program_compiled = compile_program(algod_client, clear_state_program_teal)

    print("--------------------------------------------")
    print("Deploying  Application......")

    # create new application
    app_id = create_app(algod_client, creator_private_key, approval_program_compiled, clear_state_program_compiled, global_schema, local_schema)

    # read global state of application
    print("Global state:", read_global_state(algod_client, app_id))


main()

