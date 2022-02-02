// Copyright ChoiceCoin 2022.
// Apache License
// written by Samuel Aspirin 🕵🏻‍♂️

//import javascript algosdk
const algosdk = require('algosdk');

// Configure your Algorand Client here. 
// This code was tested on the PureStake API.
const host = "https://testnet-algorand.api.purestake.io/ps2";
const puretoken = {
    "X-API-Key": "z6H94GE3sI8w100S7MyY92YMK5WIPAmD6YksRDsC"
}
const port = "";

// Initializes Client for node
const algodClient = new algosdk.Algodv2(puretoken, host, port);

// This defines an Algogenous Smart Contract for running an switch between an asset such as Choice Coin and other ASAs. 
// The Algogenous Smart Contract Integrates an embedded intelligence to automatically create a smart contract on the Algorand Blockchain certifying an switch took place.
// Connect to the Algorand Client here. 

//The fund address and fund mnemonic defined below should belong to the manager account that controls the asset that you want to offer.
const fund_address = ""
const fund_mnemonic = "" //Put the main_manager_mnemonic here.
const fund_key = algosdk.mnemonicToSecretKey(fund_mnemonic);

//receiver address and mmemonic defined below should belong to the manager account that receives the asset 
const receiver_address = ""
const receiver_mnemonic = ""// put the receiver mmemonic here
const receiver_key = algosdk.mnemonicToSecretKey(receiver_mnemonic);

//asset ID 
const ASSET_ID = 21364625

// We set revocationTarget to undefined as 
// This is not a clawback operation
const revocationTarget = undefined;
// CloseReaminerTo is set to undefined as
// we are not closing out an asset
const closeRemainderTo = undefined;
// We are sending 0 assets
const amount = 0;



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

// Function used to print asset holding for account and assetid
const printAssetHolding = async () => {
    let accountInfo = await algodClient.accountInformation(receiver_address).do();
    for (idx = 0; idx < accountInfo['assets'].length; idx++) {
        let scrutinizedAsset = accountInfo['assets'][idx];
        if (scrutinizedAsset['asset-id'] == ASSET_ID ) {
            let myassetholding = JSON.stringify(scrutinizedAsset, undefined, 2);
            console.log("assetholdinginfo = " + myassetholding);
            break;
        }
    }
};


// This defines an opt-in function for an asset. 
// It automates the optin process for user accounts who may be purschasing an asset.

const create_optin = async () => {
    const params = await algodClient.getTransactionParams().do();
    const note = undefined;
    const opt_in_txn = algosdk.makeAssetTransferTxnWithSuggestedParams(receiver_key.addr, receiver_address, closeRemainderTo, revocationTarget,amount, note, ASSET_ID, params);
    // Must be signed by the account wishing to opt in to the asset    
    let rawSignedTxn = opt_in_txn.signTxn(receiver_key.sk);
    let opt_tx = (await algodClient.sendRawTransaction(rawSignedTxn).do());

    //display in console
    console.log(`Your transaction information is at https://testnet.algoexplorer.io/tx/${opt_tx.txId}`);
 
     // wait for transaction to be confirmed
     await waitForConfirmation(opt_tx.txId);

     

     //You should now see the new asset listed in the account information
    console.log(`receiver address =  ${receiver_key.addr}`);
    //print asset holding
    await printAssetHolding();
}

create_optin();
  
