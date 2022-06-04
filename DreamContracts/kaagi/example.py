from upload import *
from download import *


def upload_file(filename: str):
    # Upload sample, returns a Transaction ID
    # needed to retrieve the file from the blockchain
    print("Procedure: Upload file to blockchain.")
    txnids = upload(
        filename=filename,
        sender_address=TEST_SENDER_ADDRESS,
        sender_private_key=TEST_SENDER_PRIVATE_KEY
    )
    fid = get_file_id(
        transaction_ids=txnids,
        receiver_address=TEST_SENDER_ADDRESS,
        sender_address=TEST_SENDER_ADDRESS,
        sender_private_key=TEST_SENDER_PRIVATE_KEY,
        post_client=init_post_client(),
        filename=filename
    )
    print(f"File ID: {fid}")
    return fid


def download_file(file_id: str):
    # Download sample, saves to current directory
    print("Procedure: Download file from blockchain.")
    download(file_id=file_id)


if __name__ == "__main__":
    # Use the following to either
    # do an upload or download
    """# Upload
    entered_fn = input("Enter filename: ")
    _file_id = upload_file(filename=entered_fn)"""

    """# Download file
    download_file(file_id=_file_id)"""
