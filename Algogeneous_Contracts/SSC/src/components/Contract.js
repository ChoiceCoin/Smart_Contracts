// Copyright Fortior Blockchain 2022
// 17 U.S.C §§ 101-1511

// importing relevant files and dependencies
import algosdk from "algosdk";
import myalgoconnect from "@randlabs/myalgo-connect";
import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { formatjsonrpcrequest } from "@json-rpc-tools/utils";
import QRCodeModal from "algorand-walletconnect-qrcode-modal";
import WalletConnect from "@walletconnect/client"; 
import './contract.scss'

//JSX Component Propose
const smartcontract = () => {
  // Starting React-dispatch to dispatch action in state in the component
  const dispatch = useDispatch();
  // Getting address from local storage
  const partyone = localStorage.getItem("address");
  const partytwo = ''

  // Starting AlgoClient Instance
  const algod_token = {"X-API-Key": ""}
  const algod_address = "";
  const headers = "";
  const ASSET_ID = 297995609;
  const algodClient = new algosdk.Algodv2(algod_token, algod_address, headers);
  const walletType = localStorage.getItem("wallet-type");
  
  const send =async() => {
    const suggestedParams = await algodClient.getTransactionParams().do();
    const agreement = document.getElementById("Agreement").value,
    const terms = document.getElementById("Terms").value,
    const amount = document.getElementById("Amount").value,
    const signature = document.getElementById("Signature").value,
    const txn =  algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
      from: partyone,
      to: partytwo,
      amount: 100000,
      assetIndex: ASSET_ID,
      suggestedParams,
    });
 
    // Building block
    return (
       <div className="smartcontract">
           <div className="create_elt">
      <div className="create_elt_inn">
        <div className="crt_hd" style={{justifyContent: "center"}}>
          <p className="converter-header"> Smart Contract </p>
        </div>
          </div>
          <div className="v_inp_cov inpCont_cand">
            <p className="inp_tit">Agreement</p>
            <input id="Agreement"
              type="text"
            />
            <p className="ensure_txt">
            Agreement.
            </p>
          </div>
          <div className="v_inp_cov inpCont_cand">
            <p className="inp_tit">Terms</p>
            <input
              type="text"
              id="Terms"
            />
            <p className="ensure_txt">
            Terms.
            </p>
          </div>
          <div className="v_inp_cov inpCont_cand">
            <p className="inp_tit">Amount</p>
            <input
              type="text"
              id="Amount"
            />
            <p className="ensure_txt">
            Amount.
            </p>
          </div> 
          <div className="v_inp_cov inpCont_cand">
            <p className="inp_tit">Signature</p>
            <input
              type="text"
              id="Signature"
            />
            <p className="ensure_txt">
            Signature.
            </p>
          </div>
            <br />
          <div className="crt_butt">
            <button onClick={SubmitContract}>Submit Smart Contract</button>
            <p className="safety" style={{textAlign : "left"}}>
            <input
                style={{cursor : "pointer", marginRight: "5px"}}
                className="checkbox"
                type="checkbox"
                value={minimumChoice}
                onClick={() => setMinimumChoice(1000000)}
              />
              By checking this box you agree to Choice Coin's <a href="https://github.com/ChoiceCoin/Compliance/blob/main/Terms_and_Conditions/TermsConditions.pdf" style={{fontSize: "11px", cursor: "pointer", marginLeft:"-5px", color:"blue"}}>Terms and Conditions.</a>
            </p>
          </div>
        </div>
      </div>
    </div>
   </div>
    );
};

export default smartcontract;