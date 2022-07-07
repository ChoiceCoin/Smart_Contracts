import hashlib


# Function to check if the uploaded file and the downloaded
# file are exactly the same. This is achieved through checking if
# the MD5 hash of the uploaded data is equal to the hash of the downloaded data
def check_circular(original: str, stitched: str):
    """
    Check if the hashes of the Original File and the Downloaded File are
    the same. This is to check if the uploaded file is complete
    and is the same with the original file that has been uploaded.

    :param original: The original file
    :param stitched: The downloaded file
    
    :return: True - hashes are the same
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
        print(f'Failed to achieve circularity.')


# Check if the expected Transaction ID
# location in the note is all in uppercase
def check_if_connection_exists(note: str):
    targ = note[(len(note)-1)-51:len(note)]
    if targ.isupper():
        return True
    else:
        return False
