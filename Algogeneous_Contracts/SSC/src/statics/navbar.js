import algosdk from "algosdk";
import { ASSET_ID } from "../constants";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState } from "react";
import MyAlgoConnect from "@randlabs/myalgo-connect";
import { CopyToClipboard } from "react-copy-to-clipboard";
import complianceLogo from '../assets/dark-compliance.png'
import corect from './correct.png';
import {Link} from 'react-router-dom';


import { PeraWalletConnect } from "@perawallet/connect";

const perawallet = new PeraWalletConnect()

const TopNavigationBar = ({ darkTheme, NavLink }) => {
  const dispatch = useDispatch();

  const addressNum = useSelector((state) => state.status.addressNum);
  const isWalletConnected =
    localStorage.getItem("wallet-type") === null ? false : true;

  const [copyToClipBoard , setCopyToClipBoard] = useState(null)

    const handyCopyToClipBoard = () => {
      setCopyToClipBoard(true)
      setTimeout(() => {
        setCopyToClipBoard(false)
  
      }, 500);
    }

  const LogOut = () => {
    perawallet.disconnect()
    localStorage.removeItem("address");
    localStorage.removeItem("addresses");
    localStorage.removeItem("wallet-type");
    localStorage.removeItem("walletconnect");
    window.location.reload();
    console.log("data");
  };

  const setMode = () => {
    if (!darkTheme) {
      localStorage.setItem("mode", "dark");
      dispatch({ type: "dark_mode" });
    } else {
      localStorage.setItem("mode", "light");
      dispatch({ type: "light_mode" });
    }
  };

  const [balance, setBalance] = useState([]);

  const algodClient = new algosdk.Algodv2(
    {
      "X-API-Key": "z6H94GE3sI8w100S7MyY92YMK5WIPAmD6YksRDsC"
    },
    "https://testnet-algorand.api.purestake.io/ps2",
    ""
  );

  const walletAddress = localStorage.getItem("address");
  const addresses = localStorage.getItem("addresses")?.split(",");

  let addrArr = [];
  

  useEffect(() => {

    addresses?.forEach(async (item) => {
      const myAccountInfo = await algodClient.accountInformation(item).do();
      const bal =
        myAccountInfo.assets.find((element) => element["asset-id"] === ASSET_ID)
          ?.amount / 100;
        
     addrArr.push({ balance: !!bal ? bal : 0, address: item });


      if(bal) {
        dispatch({
          type: "getBalance",
          balance : addrArr
        })
      }


      if (addrArr?.length === addresses?.length) {
        dispatch({
          type: "setAlgoAddress",
          addressIndex: 0,
          addr: addrArr[0]?.address,
        });
        setBalance(addrArr);
      }
    });

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const myAlgoConnect = async () => {
    const myAlgoWallet = new MyAlgoConnect({ shouldSelectOneAccount: false });

    try {
      const accounts = await myAlgoWallet.connect({
        shouldSelectOneAccount: true,
      });

      const addresses = accounts.map((item) => item?.address);
      const address = accounts[0].address;
      

      // close modal.
      localStorage.setItem("wallet-type", "my-algo");
      localStorage.setItem("address", address);
      localStorage.setItem("addresses", addresses);

      window.location.reload();
    } catch (error) {
      dispatch({
        type: "alert_modal",
          alertContent:
            "Error occurred while connecting wallet, Try again later.",
      })
      console.log(error);
    }
  };


  const peraWallet = async () => {

   const newAccounts = await perawallet.connect()
    localStorage.setItem("wallet-type", "walletconnect");
    localStorage.setItem("address", newAccounts[0]);
    localStorage.setItem("addresses", newAccounts);


    window.location.reload();
  

    
  }

  const algoSignerConnect = async () => {
    try {
      if (typeof window.AlgoSigner === "undefined") {
        window.open(
          "https://chrome.google.com/webstore/detail/algosigner/kmmolakhbgdlpkjkcjkebenjheonagdm",
          "_blank"
        );
      } else {
        await window.AlgoSigner.connect({
          ledger: "TestNet",
        });
        const accounts = await window.AlgoSigner.accounts({
          ledger: "TestNet",
        });

        const addresses = accounts.map((item) => item?.address);
        const address = accounts[0].address;

        // close modal.
        localStorage.setItem("wallet-type", "algosigner");
        localStorage.setItem("address", address);
        localStorage.setItem("addresses", addresses);

        window.location.reload();
      }
    } catch (error) {
      dispatch({
        type: "alert_modal",
        alertContent: "AlgoSigner not set up yet!",
      });
    }
  };

  return (
    <header className="small_header">
      <div className="small_header_inn">
        <Link to='/' 
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            textTransform: "uppercase",
            outline: "none"
          }}
        > 
         <img src={complianceLogo} alt="logo" style={{
           width: "30px"
         }} />
        </Link>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {!!isWalletConnected ? (
            <>
              <div className="addrDisplay">
              <li onClick={setMode}>
            
            {darkTheme ? (
              <i style={{color : 'yellow'}} className="mode uil uil-brightness-low"></i>
            ) : (
              <i className="mode uil uil-moon"></i>
            )}
          
          </li>
                
                <div className="addrDispMain">
                  
                  <div className="addrDisplayInn">
                    
                    <div className="addrBalance">
                    <li className="disconnect" style={{color: 'red', }} onClick={LogOut}>{walletAddress ? "Disconnect"  : null}</li>
                    </div>
                    

                    <CopyToClipboard text={balance[addressNum]?.address}>
                      <div className="addressTxt">
                        <p>{balance[addressNum]?.address}</p>
                        {copyToClipBoard ? (<img style={{width:'11px'}}
                          src={corect} alt="check"/>) : (<i onClick={() => handyCopyToClipBoard()} className="uil uil-copy"></i>)}
                        
                      </div>
                    </CopyToClipboard>
                  </div>
                </div>

                <div className="dropDownConnect_items">
                  {balance?.map((item, index) => {
                    return (
                      <div
                        key={index}
                        className="dropDownConnect_item"
                        onClick={() => {
                          dispatch({
                            type: "setAlgoAddress",
                            addressIndex: index,
                            addr: item.address,
                          });
                        }}
                      >
                        <p className="dropDownConnect_item_txt">
                          {item.address}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>
            </>
          ) : (
            <div className="dropDownConnect">
               <li onClick={setMode}>
            
              {darkTheme ? (
                <i style={{color : 'yellow'}} className="mode uil uil-brightness-low"></i>
              ) : (
                <i className="mode uil uil-moon"></i>
              )}
            
            </li>
              <div className="dropDownConnect_button">
                <button className="connect_wallet_button">
                  <p>
                    Connect Wallet
                    <i
                      className="uil uil-angle-down"
                      style={{ fontSize: "18px" }}
                    />
                  </p>
                </button>
              </div>

              <div className="dropDownConnect_items">
                <div className="dropDownConnect_item" onClick={myAlgoConnect}>
                  <div className="dropDownConnect_img">
                    <img
                      src="https://i.postimg.cc/76r9kXSr/My-Algo-Logo-4c21daa4.png"
                      alt=""
                    />
                  </div>
                  <p className="dropDownConnect_item_txt">My Algo Wallet</p>
                </div>

                <div
                  className="dropDownConnect_item"
                  onClick={algoSignerConnect}
                >
                  <div className="dropDownConnect_img">
                    <img
                      src="https://i.postimg.cc/L4JB4JwT/Algo-Signer-2ec35000.png"
                      alt=""
                    />
                  </div>
                  <p className="dropDownConnect_item_txt">
                    {typeof window.AlgoSigner === undefined
                      ? "Install AlgoSigner"
                      : "AlgoSigner"}
                  </p>
                </div>

                <div className="dropDownConnect_item" onClick={peraWallet}>
                  <div className="dropDownConnect_img">
                    <img
                      src="https://i.postimg.cc/QdXmHSYZ/pera.png"
                      alt=""
                    />
                  </div>
                  <p className="dropDownConnect_item_txt">
                    Pera Wallet
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="landing" id="landing">
  {/* <ScrollTextLand
        word={
          "Tita is Choice Coin Payment Gateway For ASA Governance , Make Payment and check for decentralized decisions scheduling!"
        }
      /> */}
      </div>

    
    </header>
  );
};

export default TopNavigationBar;
