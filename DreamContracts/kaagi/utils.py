# "Kaagi", a mechanism to upload and download
# files to and from the Algorand blockchain.

from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk.mnemonic import to_private_key
from algosdk.account import address_from_private_key

from urllib.request import Request, urlopen
import json
import base64

import hashlib
import os


# Initialize credentials
TEST_SENDER_MNEMONIC = os.environ['myprivkey']
TEST_SENDER_PRIVATE_KEY = to_private_key(TEST_SENDER_MNEMONIC)
TEST_SENDER_ADDRESS = address_from_private_key(TEST_SENDER_PRIVATE_KEY)
ALGONODE_NODE_ADDRESS = "http://testnet-api.algonode.network"
ALGONODE_INDX_ADDRESS = "http://testnet-idx.algonode.network"
ALGOEXPL_NODE_ADDRESS = "https://node.testnet.algoexplorerapi.io"
ALGOEXPL_INDX_ADDRESS = "https://algoindexer.testnet.algoexplorerapi.io"


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
def get_lines(note: str, max_length: int) -> list:
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


# Core upload function
def process_publishing(
        feed: str,
        receiver_address: str,
        sender_address: str,
        sender_private_key: str
) -> list:
    """
    This is the core upload procedure using the feed which is the string of
    encoded bytes from the file to be uploaded. This returns the
    Transaction IDs from submitted group transactions.

    :param feed: The raw string that is base64 encoded with encoding ISO-8859-1
    :param receiver_address: Algorand address of receiver
    :param sender_address: Algorand address of sender
    :param sender_private_key: Algorand private key of sender
    :return: txids - the Transaction IDs of submitted atomic transactions
    """
    # Initiate Algorand Client
    post_client = init_post_client()
    # Get lines from the feed
    lines = get_lines(note=feed, max_length=947)
    # Create transactions and append
    transactions = []
    # The maximum number of transactions
    # in a group transaction is 16.
    if len(lines) > 16:
        # If number of lines exceeds 16, even
        # (empty) lines are included in transaction
        # creation. Transactions are then appended
        # to the transactions list
        for line in lines:
            created_txn = create_transaction(
                post_client=post_client,
                receiver_address=receiver_address,
                sender_address=sender_address,
                message=line
            )
            transactions.append(created_txn)
            progs = round((len(transactions)/len(lines))*100, ndigits=3)
            print(f"\rPreparing..{progs}%", end="")
    else:
        # If number of lines did not exceed 16,
        # each line is included in transaction
        # creation if the length of line is not 0
        transactions = [
            create_transaction(
                post_client=post_client,
                receiver_address=receiver_address,
                sender_address=sender_address,
                message=line
            ) for line in lines if line != ""
        ]
    # Group created transactions by 16 to comply
    # with the group transaction limit of 16
    # individual transactions per group
    init_lines = []
    actual_lines = []
    if len(lines) > 16:
        for eachtxn in transactions:
            init_lines.append(eachtxn)
            if len(init_lines) == 16:
                actual_lines.append(init_lines)
                init_lines = []
            progs = round(((transactions.index(eachtxn)+1)/len(transactions)*100), ndigits=3)
            print(f"\rAppending..{progs}%", end="")
        # If the last batch of transactions are out and
        # their number did not reach 16, append to
        # actual lines nonetheless.
        if len(init_lines) != 0:
            actual_lines.append(init_lines)
    else:
        # If the length of main line is less than 16,
        # bypass the sorting so that the actual lines
        # becomes the list of transactions
        actual_lines = [transactions]
    # Calculate Group IDs for
    # each subgroup in transactions list
    # and append to a signed transactions list
    signed_transactions = []
    signed_transactions_process = []
    print(f'\nCalculating GIDs..')
    for group in actual_lines:
        # Calculate Group ID for each batch of transactions
        cgid = transaction.calculate_group_id(txns=group)
        for inner_item in group:
            # Assign calculated Group ID
            # to each transaction
            inner_item.group = cgid
            # Sign transaction
            signed_txn = inner_item.sign(sender_private_key)
            # Add to processing list
            signed_transactions_process.append(signed_txn)
        # Append to final signed_transactions list
        signed_transactions.append(signed_transactions_process)
        # Reset helper list
        signed_transactions_process = []
    # Send signed group transactions to the Algorand blockchain
    txids = []
    for signed_group in signed_transactions:
        txid = post_client.send_transactions(signed_group)
        txids.append(txid)
        # Do not wait for confirmation
        progs = round(((signed_transactions.index(signed_group)+1)/len(signed_transactions)) * 100, 3)
        print(f"\rSubmitted transactions..{progs}% ", end="")
    return txids


# This function is to assemble
# the notes from each transaction
# in the upload procedure to
# produce the same uploaded file
def stitch_records(
        get_client: AlgodClient,
        txn_ids: list,
) -> str:
    """
    Stitches notes from raw Transaction IDs
    obtained from the upload procedure

    :param get_client: AlgodClient (GET)
    :param txn_ids: Transaction IDs from upload procedure
    :return: stitched - the Stitched Records (string)
    """
    stitched = ""
    stitched_initial_list = []
    for specific_txid in txn_ids:
        while True:
            # Search note based on given Transaction ID
            obtained_note = search_note_by_txid(
                get_client=get_client,
                txid=specific_txid
            )
            if obtained_note is not None:
                # Append to list if note is found
                stitched_initial_list.append(obtained_note)
                now = txn_ids.index(specific_txid)+1
                mot = len(txn_ids)
                num = round((now/mot)*100, 3)
                print(f"\r({num}%) Stitching... ", end="")
                break
    # Once all the notes are obtained,
    # place them all in one single
    # string and return
    for sil in stitched_initial_list:
        stitched += sil
    return stitched


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
        now = txids.index(txid) + 1
        mot = len(txids)
        num = round((now / mot) * 100, 3)
        print(f'\rFetching infos...{num}% ', end='')
        try:
            req = f'/v2/transactions/{txid}'
            url = client.algod_address + req
            request = Request(url, headers=client.headers)
            while True:
                resp = urlopen(request)
                json_loaded = json.load(resp)
                if len(str(json_loaded)) > 0 and str(json_loaded) != "()":
                    jsons.append(json_loaded)
                    break
        except Exception as e:
            print(e.args)
    return jsons


def get_confirmed_rounds_from_txid(txids: list, client: AlgodClient):
    confirmed_rounds = []
    # Get confirmed round
    try:
        while True:
            tx_infos = get_transaction_info(txids=txids, client=client)
            if len(tx_infos) > 0:
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


# Vital function to check if
# the uploaded file and downloaded
# file are exactly the same. This
# is achieved through checking if
# the hash of the uploaded data is
# equal to the hash of the
# downloaded data
def check_circular(original: str, stitched: str):
    """
    Check if hashes of Original File and Downloaded File are
    the same. This is to check if the uploaded file is complete
    and is the same with the original file that has been uploaded.

    :param original: The original file.
    :param stitched: The downloaded file.
    :return: Returns True if original and downloaded hashes are the same.
    """
    print(f'\nChecking circularity...')
    stitched_hash = hashlib.md5(stitched.encode()).hexdigest()
    original_hash = hashlib.md5(original.encode()).hexdigest()
    if stitched_hash == original_hash:
        print('Achieved circularity.')
        return True
    else:
        print(f'Length of original: {len(original)} Hash: {original_hash}')
        print(f'Length of stitched: {len(stitched)} Hash: {stitched_hash}')
        print(f'Circularity not achieved. Try again.')


# Main upload function
def upload(
        filename: str,
        sender_address: str,
        sender_private_key: str
):
    """
    Uploads certain local file to blockchain and returns only if
    the uploaded file is found to be the same with the downloaded file.

    :param filename: The filename of the file to be uploaded
    :param sender_address: Algorand address of sender
    :param sender_private_key: Algorand private key of sender
    :return: downloaded_file: The stitched records from Algorand blockchain
    :return: transaction_ids: Transaction IDs submitted to the blockchain
    """
    # Base64 encode the bytes and decode to get the string
    with open(filename, 'rb') as o:
        original_file = o.read().decode('ISO-8859-1')
        original_file = base64.b64encode(original_file.encode()).decode()
    print(f'Uploading {filename} to Algorand blockchain..')
    # Get Transaction IDs submitted to the blockchain
    transaction_ids = process_publishing(
        feed=original_file,
        receiver_address=sender_address,
        sender_address=sender_address,
        sender_private_key=sender_private_key
    )
    # Initialize GET Client
    get_client = init_get_client()
    # Loop until downloaded data is exactly
    # the same with the uploaded data
    while True:
        # Get Transaction IDs from Transaction IDs
        txn_ids = get_txn_ids_from_txn_id(
            __txids=transaction_ids,
            client=get_client
        )
        # Download the uploaded file from the blockchain
        downloaded_file = stitch_records(
            get_client=get_client,
            txn_ids=txn_ids
        )
        # Check if the uploaded file
        # and downloaded file are the same
        # and return Transaction IDs from
        # upload procedure if so
        circular = check_circular(
            original=original_file,
            stitched=downloaded_file
        )
        if circular:
            print('File successfully uploaded to blockchain.')
            return transaction_ids


# Main download procedure
def download(file_id: str):
    """
    Download file from blockchain using the
    File ID generated from upload procedure

    :param file_id: The link which is a File ID generated from upload.
    :return: None, after downloading, the downloaded file will be in the same directory.
    """
    # Initialize stuff to be used later
    get_client = init_get_client()
    remnant = []
    first = True
    connection = None
    fno = None
    fno_decoded = None
    # Repeat until there is no Connection left.
    # A Connection is the Transaction ID
    # included at the end of a note to serve as
    # a link to the preceding note.
    while True:
        if first:
            gotten = search_note_by_txid(
                get_client=get_client,
                txid=file_id
            )
            first = False
        else:
            gotten = search_note_by_txid(
                get_client=get_client,
                txid=connection
            )
        if gotten != "":
            has_connection = check_if_connection_exists(gotten)
            # Check if a Transaction ID is
            # expected to be found in the note,
            # thus hinting that there is a preceding
            # note. if "<fn>" is found in the note,
            # it means that the there are no more
            # preceding notes.
            if has_connection and not ("<fn>" in gotten):
                connection = gotten[(len(gotten)-1)-51:]
                actual = gotten[:(len(gotten)-1)-51]
                remnant.append(actual)
            else:
                actual = gotten[:]
                remnant.append(actual)
                break
        else:
            break
    # Arrange the reference line
    # to link other Transaction IDs
    remnant.reverse()
    omega = ""
    for particle in remnant:
        omega += particle
        if "<fn>" in particle:
            sidx = particle.index("<fn>")
            idxstart_of_fn = sidx + 4
            idxend_of_fn = idxstart_of_fn
            # Get index of end of filename
            while particle[idxend_of_fn] != "<":
                idxend_of_fn += 1
            # Get filename
            fno = particle[idxstart_of_fn:idxend_of_fn]
            fno_decoded = base64.b64decode(fno.encode()).decode('iso-8859-1')
            print(f"File name: {fno_decoded} ")
            print(f"File ID: {file_id}")
            print(f"File description: ")
        # An algorithm can be inserted here to get
        # the file description if there is one included
    filename_whole = f"<fn>{fno}</fn>"
    if filename_whole in omega:
        omega = omega.replace(filename_whole, "")
    else:
        print("Cannot edit omega")
    transaction_ids = get_lines(
        note=omega,
        max_length=52
    )
    while True:
        try:
            # Get Transaction IDs from the
            # Transaction IDs obtained from the File ID
            txn_ids = get_txn_ids_from_txn_id(
                __txids=transaction_ids,
                client=get_client
            )
            # Download the file from the blockchain
            downloaded_file = stitch_records(
                get_client=get_client,
                txn_ids=txn_ids
            )
            # Write the downloaded file to disk
            if len(downloaded_file) != 0:
                write_to_file(
                    input_data=downloaded_file,
                    file_name_out=fno_decoded
                )
                break
        except Exception as err:
            print(err.args)


# This function is to get the File ID
# that can be used to download the data
# from the blockchain using the functions
# in this module
def get_file_id(
        transaction_ids: list,
        receiver_address: str,
        sender_address: str,
        sender_private_key: str,
        post_client: AlgodClient,
        filename: str,
) -> str:
    """
    Returns a link which is essentially a Transaction ID
    that can be used to download the uploaded file.

    :param transaction_ids: Transaction IDs from upload
    :param receiver_address: Algorand address of receiver
    :param sender_address: Algorand address of sender
    :param sender_private_key: Private key of sender
    :param post_client: AlgodClient to node (not indexer)
    :param filename: filename of the uploaded file
    :return: File ID (a Transaction ID) used for stitching
    """
    print(f"Assigning File ID...Please Wait...")
    alpha_fn = base64.b64encode(filename.encode()).decode()
    alpha = f"<fn>{alpha_fn}</fn>"
    for txid in transaction_ids:
        alpha += txid
    feed = get_lines(
        note=alpha,
        max_length=947
    )
    txid = None
    for each in feed:
        if len(each) != 0:
            if len(feed) > 1:
                if txid is None:
                    txn = create_transaction(
                        post_client,
                        receiver_address,
                        sender_address,
                        message=each
                    )
                else:
                    txn = create_transaction(
                        post_client,
                        receiver_address,
                        sender_address,
                        message=each+txid
                    )
                sgd = txn.sign(sender_private_key)
                txid = post_client.send_transaction(sgd)
                transaction.wait_for_confirmation(
                    algod_client=post_client,
                    txid=txid
                )
            else:
                txn = create_transaction(
                    post_client,
                    receiver_address,
                    sender_address,
                    message=each
                )
                sgd = txn.sign(sender_private_key)
                txid = post_client.send_transaction(sgd)
                transaction.wait_for_confirmation(
                    algod_client=post_client,
                    txid=txid
                )
    return txid


# Check if the expected Transaction ID
# location in the note is all in uppercase
def check_if_connection_exists(note: str):
    targ = note[(len(note)-1)-51:len(note)]
    if targ.isupper():
        return True
    else:
        return False


# The final phase of downloading
# the file from the blockchain. This
# function will write the downloaded
# data from the blockchain to disk
def write_to_file(input_data: str, file_name_out: str):
    """
    Write the downloaded file from blockchain to disk.

    :param input_data: The downloaded data from blockchain
    :param file_name_out: Filename of output file
    """
    with open(file_name_out, 'wb') as f:
        to_be = base64.b64decode(input_data).decode()
        f.write(to_be.encode("ISO-8859-1"))
        print(f'\nDownloaded file: {file_name_out} to current directory')


if __name__ == '__main__':
    pass
