// Copyright ChoiceCoin 2022.
// Apache License

// This code defines an asset creation process on the Algorand Blockchain. 
// It is configured to create Choice Coin, however, the asset_details may be altered.

//import javascript algosdk
const algosdk = require('algosdk');

// Configure your Algorand Client here. 
// This code was tested on the PureStake API.
const host = "https://testnet-algorand.api.purestake.io/ps2";
const puretoken = {
    "X-API-Key": ""
}
const port = "";

// Initializes Client for node
const algodClient = new algosdk.Algodv2(puretoken, host, port);

// create testnet account and put your wallet address
const creator_address = "" // Put in main creator address here. This is the account that you want to be the manager of the asset.
const creator_mnemonic = "" // the mmemonic 25 characters seperated by a whitespace should be imported here
const creator_key = algosdk.mnemonicToSecretKey(creator_mnemonic);

// Details of the asset creation transaction.
// Alter these details as you wish. 
// Keep the manager, reserve, freeze, and clawback address the same as these point back to the variable defined at the beginning.
const defaultFrozen = false;
const unitName = "choice";
const assetName = "ChoiceCoin";
const url = ""; //url to the asset
const managerAddr = creator_address;
const reserveAddr = creator_address;
const freezeAddr = creator_address;
const clawbackAddr = creator_address;
const metadata = undefined;
const total = 1; 
const decimals = 10; 

//wait for it to sync to algorand blockchain
const waitForConfirmation = async (txId) =>  {
    let response = await algodClient.status().do();
    let lastround = response["last-round"];
    while (true) {
        const pendingInfo = await algodClient.pendingTransactionInformation(txId).do();
        if (pendingInfo["confirmed-round"] !== null && pendingInfo["confirmed-round"] > 0) {
            //Got the completed Transaction
            console.log("Transaction " + txId + " confirmed in round " + pendingInfo["confirmed-round"]);
            break;
        }
        lastround++;
        await algodClient.statusAfterBlock(lastround).do();
    }
};


// Creates the asset.
// To run on the Terminal, import the creator_address,creator_key,and the creator_mnemonic.
// Finally, import the create_asset function and run as specified (without any inputs). 
// Go to the algoexplorer link that is returned to get a validated transaction. Record the asset_id and any other details you want.

const create_asset = async () => {
    const params = await algodClient.getTransactionParams().do();
            
    const txn = algosdk.makeAssetCreateTxnWithSuggestedParamsFromObject({
    from: creator_address,
    total,
    decimals,
    assetName,
    unitName,
    assetURL: url,
    assetMetadataHash: metadata,
    defaultFrozen,
    freeze: freezeAddr,
    manager: managerAddr,
    clawback: clawbackAddr,
    reserve: reserveAddr,
    suggestedParams: params,
    });

    let rawSignedTxn = txn.signTxn(creator_key.sk)
    let tx = (await algodClient.sendRawTransaction(rawSignedTxn).do());

    let assetID = null;

    //information in the console
    console.log(`Your transaction information is at https://testnet.algoexplorer.io/tx/${tx.txId}`);

    // wait for transaction to be confirmed
    await waitForConfirmation(tx.txId);

    
    // Get the new asset's information from the creator account
    let ptx = await algodClient.pendingTransactionInformation(tx.txId).do();
    assetID = ptx["asset-index"];
    console.log('assetID', assetID);
}

create_asset()

   
