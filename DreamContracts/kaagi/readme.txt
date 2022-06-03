"Kaagi" - A mechanism to upload and download files to and from the Algorand blockchain.

Important note: 
As it is known that Algorand blockchain is a permissionless, public blockchain,
it is determined that all data in the blockchain are accessible by any user. Thus,
kindly use this program at your own discretion. Uploading sensitive or private
data is highly discouraged. However, a sample file (sample-file.txt) is included
in this folder for testing and demonstration purposes.

This folder contains the following:
> utils.py
> upload.py
> download.py

utils.py contains the functions needed to
successfully perform an upload and a download
of a local file to the blockchain.

upload.py contains a sample code demonstrating
the upload process.

download.py contains a sample code demonstrating
the download process.

To perform a file upload, run upload.py.
To perform a file download, run download.py.

Additional notes:
Any kind of file can be uploaded to the blockchain
(e.g. .mp3, .pdf, .docx, .html, .mp4, etc.) but
consider that larger files may take a significant 
amount of time to upload. Even so, an error may
be encountered when uploading large files (>6mb) in 
size.
