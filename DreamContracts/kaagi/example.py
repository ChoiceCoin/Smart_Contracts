from upload import TEST_SENDER_ADDRESS, TEST_SENDER_PRIVATE_KEY, get_file_id, upload, init_post_client
from download import download


# Upload file, returns a Transaction ID
# needed to retrieve the file from the blockchain
# The file must be in the same directory else 
# an external file from other directory must be 
# written to the current directory before uploading
def upload_file(filename: str):
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


# Download file, saves to current directory
def download_file(file_id: str):
    print(f"Downloading {file_id} from the blockchain")
    download(file_id=file_id)


if __name__ == "__main__":
    while True:
        selection = int(input("Download or upload? (0 - Download, 1 - Upload) "))
        if selection == 0 or selection == 1:
            break
    if selection == 1:
        # Upload file
        entered_fn = input("Enter filename: ")
        fid = upload_file(filename=entered_fn)
    if selection == 0:
        # Download file
        entered_id = input("Enter file id (generic algorand txid): ")
        download_file(file_id=entered_id)
