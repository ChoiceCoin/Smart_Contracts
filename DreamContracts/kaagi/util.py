from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.mnemonic import to_private_key
from algosdk.account import address_from_private_key
from urllib.request import Request, urlopen
import json
import base64
import os

from constants import *

TEST_SENDER_MNEMONIC = os.environ['mymnemonic']
TEST_SENDER_PRIVATE_KEY = to_private_key(TEST_SENDER_MNEMONIC)
TEST_SENDER_ADDRESS = address_from_private_key(TEST_SENDER_PRIVATE_KEY)


def init_post_client():
    """
    Initializes an Algorand Client for posting data

    :return: algod_client - AlgodClient (POST)
    """
    algod_address = ALGONODE_NODE_ADDRESS
    algod_token = ''
    headers = {'User-Agent': 'algosdk'}
    algod_client = AlgodClient(algod_token, algod_address, headers)
    return algod_client


def init_get_client():
    """
    Initializes an Algorand Client for getting data

    :return: algod_client - AlgodClient (GET)
    """
    algod_address = ALGONODE_INDX_ADDRESS
    algod_token = ''
    headers = {'User-Agent': 'algosdk'}
    algod_client = AlgodClient(algod_token, algod_address, headers)
    return algod_client


def get_account_info(
        get_client: AlgodClient,
        account_address: str
):
    """
    Gets account information from the given account address.

    :param get_client: AlgodClient (GET)
    :param account_address: Algorand public address of target account
    :return: info - Account information
    """
    info = None
    while True:
        try:
            info = get_client.account_info(address=account_address)
            if info is not None:
                return info
        except Exception as err:
            print(err.args)
        finally:
            if info is None:
                info = get_client.account_info(address=account_address)
                if info is not None:
                    return info


# Notes in payment transactions are
# utilized to store data in the blockchain
def create_transaction(
    post_client: AlgodClient,
    receiver_address: str,
    sender_address: str,
    message
):
    """
    Creates a payment transaction for a given message.

    :param post_client: AlgodClient (POST)
    :param receiver_address: Algorand receiver address
    :param sender_address: Algorand sender address
    :param message: The note
    :return: A payment transaction (PaymentTxn)
    """
    return transaction.PaymentTxn(
        sender=sender_address,
        sp=post_client.suggested_params(),
        receiver=receiver_address,
        amt=0,
        note=message
    )


# Because data is stored in notes,
# the following function gets the note
# of a given transaction.
def search_note_by_txid(
        get_client: AlgodClient,
        txid: str
):
    """
    Gets note based on the specified Transaction ID

    :param get_client: AlgodClient (GET)
    :param txid: Transaction ID from which to get the note
    :return: note - the note of a given transaction
    """
    try:
        while True:
            req = f'/v2/transactions/{txid}'
            url = get_client.algod_address + req
            request = Request(url=url, headers=get_client.headers)
            resp = urlopen(request)
            json_loaded = json.load(resp)
            note = str(json_loaded['transaction']['note'])
            # Notes are base64 decoded as it is
            # base64 encoded before uploading to the
            # blockchain. This is to add a layer of
            # obfuscation to the contents of the actual
            # note. This can be edited so as not to
            # do base64 encoding before uploading thereby
            # not needing to decode when it is fetched from
            # the blockchain.
            note = base64.b64decode(note).decode()
            if len(note) != 0:
                return note
    except Exception as e:
        print(e.args)


# Since there is limited length of bytes per note in the
# transaction which is 1024 bytes or 1 kilobyte, the main feed
# of bytes obtained from encoding of the file-to-be-uploaded is
# divided into separate lines
def get_lines(
        note: str,
        max_length: int
) -> list:
    """
    Get lines for each transaction. Each line, by design, is 947 bytes in length,
    max length is 1024 bytes for the Algorand note field.

    :param note: The main feed which is base64 encoded with ISO-8859-1 encoding
    :param max_length: The intended line length
    :return: list_of_notes - A list of notes
    """
    # Do first append
    list_of_notes = [note[0:max_length]]
    new_note = note[max_length:]
    # Repeat succeeding appends
    while True:
        list_of_notes.append(new_note[0:max_length])
        new_note = new_note[max_length:]
        # Do append if final line is reached
        if len(new_note) < max_length:
            list_of_notes.append(new_note[0:])
            break
    return list_of_notes


def get_transaction_info(
        txids: list,
        client: AlgodClient
):
    """
    Gets transaction infos from transaction IDs

    :param txids: Transaction IDs
    :param client: AlgodClient (GET -> directed to indexer)
    :return: jsons: Transaction Infos
    """
    jsons = []
    for txid in txids:
        try:
            req = f'/v2/transactions/{txid}'
            url = client.algod_address + req
            request = Request(url, headers=client.headers)
            while True:
                resp = urlopen(request)
                json_loaded = json.load(resp)
                if len(str(json_loaded)) > 0 and str(json_loaded) != "()":
                    jsons.append(json_loaded)
                    print(f"\rFetched infos...", end="")
                    break
        except Exception as e:
            print(e.args)
    return jsons


def get_confirmed_rounds_from_txid(
        txids: list,
        client: AlgodClient
):
    confirmed_rounds = []
    # Get confirmed round
    try:
        while True:
            tx_infos = get_transaction_info(txids=txids, client=client)
            if len(tx_infos) != 0:
                break
        for txinfo in tx_infos:
            while True:
                conrnd = str(txinfo['transaction']['confirmed-round'])
                if len(conrnd) > 0:
                    confirmed_rounds.append(conrnd)
                    break
    except Exception as e:
        print(e.args)
    return confirmed_rounds


def get_txn_ids_from_txn_id(
        __txids: list,
        client: AlgodClient
):
    """
    Gets Transaction IDs from a Transaction ID,
    leverages Confirmed Rounds and Group IDs.

    :param __txids: Transaction IDs
    :param client: AlgodClient (GET -> directed to indexer)
    :return: txids: Transaction IDs
    """
    txids = []
    initial = []
    bridge_for_reverse = []
    block_infos = []
    while True:
        try:
            # Get confirmed rounds
            while True:
                confirmed_rounds = get_confirmed_rounds_from_txid(
                    txids=__txids,
                    client=client
                )
                if len(confirmed_rounds) > 0:
                    break
            print("\rGoing through blocks... ", end="")
            while True:
                # Get block infos
                for cround in confirmed_rounds:
                    req = f'/v2/transactions?round={cround}'
                    url = client.algod_address + req
                    request = Request(url, headers=client.headers)
                    while True:
                        resp = urlopen(request)
                        json_loaded = str(json.load(resp))
                        if len(json_loaded) > 0:
                            block_infos.append(json_loaded)
                            break
                # Get Group ID list
                gids = get_group_id(client=client, txids=__txids)
                # Get Transaction IDs
                for index, block_info in enumerate(block_infos, start=0):
                    while gids[index] in block_info:
                        gid_index = block_info.find(gids[index])
                        full_gid_index = gid_index + len(gids[index])
                        gid_ = block_info[gid_index:full_gid_index]
                        gid_and_ = gid_ + '","id":"'
                        txid_start_index = (gid_index + 1) + (len(gid_and_) + 1)
                        txid_end_index = txid_start_index + 52
                        txid_extract = block_info[txid_start_index:txid_end_index]
                        initial.append(txid_extract)
                        block_info = block_info[txid_end_index+1:]
                    txids.append(initial)
                    initial = []
                break
            break
        except Exception as e:
            print(e.args)
    txids.reverse()
    for sublist in txids:
        bridge_for_reverse.append(sublist)
    txids = []
    bridge_for_reverse.reverse()
    for superior in bridge_for_reverse:
        for inferior in superior:
            txids.append(inferior)
    return txids


# Group IDs are used to find
# other Transaction IDs from
# the given Transaction IDs
# obtained from the upload
# procedure
def get_group_id(
        client: AlgodClient,
        txids: list
) -> list:
    """
    Gets Group IDs from Transaction IDs

    :param client: an AlgodClient (GET)
    :param txids: Transaction IDs
    :return: gids - Group IDs
    """
    # Get Group IDs
    gids = []
    print("Getting gids...")
    try:
        while True:
            txn_infos = get_transaction_info(
                txids=txids,
                client=client
            )
            if len(txn_infos) != 0:
                for txn_info in txn_infos:
                    gid = txn_info['transaction']['group']
                    if len(gid) > 0:
                        gids.append(gid)
                break
    except Exception as e:
        print(e.args)
    return gids
