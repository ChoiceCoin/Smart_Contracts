from util import *
from stitching import stitch_records
from checking import check_circular


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


# Link getter
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
    print(f"Assigning File ID...Please Wait.")
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
