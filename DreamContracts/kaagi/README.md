# Kaagi
This is a mechanism to upload and download a file to and from the Algorand blockchain.

## The Upload
The upload outputs a Transaction ID that represents the file uploaded
in the blockchain. This is done through spreading the contents of the file into 
many parts and sent as notes among different transactions. 

The upload process is completed after being able to stitch back the parts of the 
file into one piece. A download is performed to see if both hashes of the downloaded file
and the original file are the same. This is to ensure that the file uploaded 
to the blockchain is exactly the same with the original file, hence achieving circularity.

## The Download
The download works by using the generated Transaction ID from the upload to 
"stitch" back the contents of the file. There is no need to check for circularity 
as the file was finalized to be the same with the original file in the upload process.

## Usage
Download this repo and use example.py to demonstrate the upload and download functions.

## Note
As it is known that Algorand blockchain is a permissionless, public blockchain,
it is determined that any data in the blockchain is accessible by any user. Thus,
kindly use this at your own discretion. Uploading sensitive or private data is 
highly discouraged. 

A sample file is included in this folder for testing and demonstration 
purposes. Any kind of file can be uploaded to the blockchain (e.g. .mp3, .pdf, .docx, 
.html, .mp4, etc.) but consider that larger files may take a significant amount of time 
to upload. Even so, an error may be encountered when uploading larger files (>7mb) in size.
