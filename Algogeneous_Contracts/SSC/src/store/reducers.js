import { combineReducers } from "redux";

const status = (
  state = {
    darkTheme: localStorage.getItem("mode") === "light" ? false : true,
    alertModal: { openModal: false, modalContent: "", percentage: "", txId: ""},
    electModal: { openElectModal: false, modalData: null },
    voteModal: { openModalVote: false, voteData: null },
    confirmWallet: { openWallet: false, walletContent: ""},
    formAlert: {formAlert: false, alertContent: ""},
    addressNum: 0,
    address: null,
    balance : 0
  },
  action
) => {
  switch (action.type) {
    
    case "getBalance" : 
      return {...state, balance : action.balance}

    case "setAlgoAddress" : 
      localStorage.setItem("address", `${action?.addr}`);
      return { ...state, addressNum: action.addressIndex };

    case "light_mode":
      return { ...state, darkTheme: false };
    case "dark_mode":
      return { ...state, darkTheme: true };

    case "alert_modal":
      return {
        ...state,
        alertModal: { openModal: true, modalContent: action.alertContent, percentage: action.percentage, txId: action.txId },
      };

    case "close_modal":
      return { ...state, alertModal: { openModal: false, modalContent: "", percentage: "", txId: "" } };

      case "confirm_wallet":
        return {...state, confirmWallet : { openWallet : true, walletContent: action.alertContent }} ; 
  
      case "close_wallet" :
        return {...state, confirmWallet : {openWallet : false, walletContent : ""} };

      case "form_alert" :
        return {...state, formAlert: {formAlert: true, alertContent: action.alertContent}};
      case "close_alert" :
        return { ...state, formAlert : {formAlert: false, alertContent : ""}};

    default:
      return state;
  }
};

export default combineReducers({ status });
