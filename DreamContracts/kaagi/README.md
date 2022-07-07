# Kaagi
This is a mechanism to upload/download any file to/from the Algorand blockchain.

## Uploading Files
The upload outputs a Transaction ID that represents the file that was uploaded
to the blockchain. This is done through dividing the contents of the file into 
many parts and sent as notes among different transactions. 

The upload process is completed after the algorithm successfully "stitches" back the
file into one piece. This is confirmed through performance of a download 
to see if both hashes of the downloaded file and the original file are the same. This is to 
ensure that the file uploaded to the blockchain is exactly the same with the original file to achieve circularity.

## Downloading Files
The download works by using the Transaction ID from the upload process to 
"stitch" back the contents of the file. There is no need to check for circularity 
as the file was confirmed to be the same with the original file in the before the upload
process was finished.

The File ID is basically an Algorand Transaction ID. Any file previously uploaded can be
downloaded back using the transaction ID outputted from the upload process.

## Usage
1. Download this folder.
2. Install required packages via ```pip install -r requirements.txt```.
3. Edit your Environment Variables -> add variable named "mymnemonic" with value which is your test account mnemonic. Make sure to fund this account with TestNet ALGOs via https://bank.testnet.algorand.network/.
4. Run example.py through ```python example.py``` in the terminal.

Running example.py will let the user input ```0``` for download, ```1``` for upload. 
If download is preferred, the program will ask for the File ID. On the other hand,
if upload is chosen, the program will ask for the user to enter the filename. Make sure 
that the file-to-be-uploaded is in the same directory where example.py is located.

## Note
As it is known that Algorand blockchain is a permissionless, public blockchain,
it is determined that any data in the blockchain is accessible by any user. Thus,
kindly use this at your own discretion. Uploading sensitive or private data is 
highly discouraged. 

A sample file is included in this folder for testing and demonstration 
purposes. Any kind of file can be uploaded to the blockchain (e.g. .mp3, .pdf, .docx, 
.html, .mp4, etc.) but consider that larger files may take a significant amount of time 
to upload. Even so, an error may be encountered when uploading larger files (>7mb) in size.
