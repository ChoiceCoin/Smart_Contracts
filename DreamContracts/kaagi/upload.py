from utils import *


if __name__ == "__main__":
    # Upload sample, prints a Transaction ID
    # needed to retrieve the file from the blockchain
    fname = input('Enter file name to upload: ')
    txnids = upload(
        filename=fname,
        sender_address=TEST_SENDER_ADDRESS,
        sender_private_key=TEST_SENDER_PRIVATE_KEY
    )
    fid = get_file_id(
        transaction_ids=txnids,
        receiver_address=TEST_SENDER_ADDRESS,
        sender_address=TEST_SENDER_ADDRESS,
        sender_private_key=TEST_SENDER_PRIVATE_KEY,
        post_client=init_post_client(),
        filename=fname
    )
    print(f"File ID: {fid}")
