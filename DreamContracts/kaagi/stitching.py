from util import *


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
