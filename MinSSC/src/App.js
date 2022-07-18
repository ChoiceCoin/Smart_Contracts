// Imports
import './App.css';
//import algosdk from "algosdk";

// Smart Contract
function SmartContract() {
   // Algorand Network Connection
   const algod_token = {
    'X-API-Key': ''
  }
  const algod_address = '';
  const headers = '';
  const ASSET_ID = 297995609;
  //const algodClient = new algosdk.Algodv2(algod_token, algod_address, headers);
  const serviceAddress = ''

  // Contract
  const contract = () => {
    console.log('Smart Contract')
  }
  return (
    <button onClick={contract}>Submit Contract</button>
  )
};

// Wallet Connect
function WalletConnect() {
  const wallet = () => {
    console.log('Connect')
  }
  return(
    <button onClick={wallet}>Connect Wallet</button>
  )
};

// React functions must return a React component
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          Choice Coin Smart Contract
        </h1>
        <label>
          First Party:
        <input type="text" name="name" />
        </label>
        <label>
          Second Party:
        <input type="text" name="name" />
        </label>
        <label>
          Terms:
        <input type="text" name="name" />
        </label>
        <label>
          Signature:
        <input type="text" name="name" />
        </label>
        <div>
        <WalletConnect />
        </div>
        <div>
        <SmartContract />
        </div>
      </header>
    </div>
  );

}

export default App;
