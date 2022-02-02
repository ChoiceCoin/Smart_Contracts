# Smart-Contracts

## check video on youtube

- [youtube](https://www.youtube.com/watch?v=Q4UQeHZJuY0)

## Requirements
* NPM and Node installed, download [HERE](https://phoenixnap.com/kb/install-node-js-npm-on-windows)
* A Purestake API key: [See Tutorial](https://developer.algorand.org/tutorials/getting-started-purestake-api-service/)
* Funded Testnet Accounts: [See Tutorial](https://developer.algorand.org/tutorials/create-account-testnet-javascript/)

## Run Application On Your Local Machine

* git clone the repository

```
  $ git clone https://github.com/ChoiceCoin/Smart_Contracts.git
```
* go into the smart contracts directory

```
 $ cd Smart_Contracts
```
* install app dependencies
```
 $ npm install
```

* create asset_ID, update the following in `asset_creation.js` file

```
const token = {
  "X-API-Key": "" //your API key gotten from purestake API, 
}

const creator_mnemonic = ""; //the mmemonic 25 characters seperated by a whitespace should be imported here

const creator_address = "" 

```

* start `asset_creation.js` script in the terminal

```
$ node asset_creation.js
```

* optn-in already created assetID, update the following in `algoG.js` file

```
const ASSET_ID = "" //add asset Id 

const token = {
  "X-API-Key": "" //your API key gotten from purestake API, 
}

const receiver_mnemonic = ""; //the mmemonic 25 characters seperated by a whitespace should be imported here

const receiver_address = "" 

```
* start `algoG.js` script in the terminal

```
$ node algoG.js
```


