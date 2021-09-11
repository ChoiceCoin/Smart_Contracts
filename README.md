# Smart Contacts
This Repository is dedicated to code for Alogrand Smart Contracts using Choice Coin. Read Docs for how to implement Algogenous Smart Contracts for your own applications. Smart contracts are programs that automatically execute, transferring cryptocurrency between parties.  In other words, smart contracts are logically executed on a blockchain to transfer assets without only computational or formalized oversight.  Algorand Smart Contracts (ASCs) allow for global payments and financial transactions, with instantaneous processing and only marginal fees – less than $0.01 in total value. As typically described the three types of ASCs are: (1) Stateful Smart Contracts; (2) Stateless Smart Contracts; and (3) Algogeneous Smart Contracts.

# Stateful
Stateful refers to the contract’s ability to store information in a specific state on the network. For example, one type of stateful smart contract is a request payment function, allowing a user to request payment from another user. Generally, Stateful Smart Contracts are logical programs which store data on the blockchain.

# Stateless
Stateless Smart Contracts differ in that they validate transactions between parties, like an escrow and more like a contract in the traditional sense. Stateless Smart Contracts on the Algorand Network also act as signature delegators,  signing transactions, thus validating them on the main blockchain network. By analogy, many describe Stateless Smart Contracts as essentially equivalent to escrow functions.  Indeed, the essential design purpose for Stateless Smart Contracts were to approve or deny blockchain transactions.

# Algogeneous
Representing a technical convergence of Stateless and Stateful Smart Contracts, Algogeneous Smart Contracts include an innovative integration with artificial intelligence. Where previous ASCs must be stateful or stateless, Algogeneous contracts may be stateful, stateless, or both.

# Docs

# Files

- The “Algogenous_Contracts” Folder contains examples of  Algogenous Smart Contracts.
- The “Single_State_Contracts” Folder contains examples of Stateful and Stateless Contracts.




# Dependencies
- To run the code in the Algogenous_Contracts Folder, you first must have Python installed. Please download the latest version of Python, and create a virutal environment specifcally for this directory. Python Download: https://www.python.org/downloads/.
- Second, your Python Virtual Envrionment must have all of the packages listed in the *requirements.txt* file, which is also found in the Algogenous_Contracts Folder.

# Run Steps
- To run the code found in the *Algogenous_Contracts* folder, make sure to first download the dependencies as described above using *pip*.
- Use Choice Coin or create a new Algorand Standard Asset as described in the *asset_creation.py* file in the *Algogenous_Contracts* folder. Once this is done, change the value of *asset_id* in the *AlgoG.py* file to the id of the asset you just created. Additionally, assign the manager address and mnemonic to the *fund_address* and *fund_mnemonic* variables in the *AlgoG.py* file. 
- Furthermore, connect to the Algorand Network through a service such as the PureStake API or the Algorand Sandbox, the code was tested using the PureStake API, and assign your new address and token to *algod_address* and *algod_token* respectively.
- In the *algo_switch* function, found in *AlgoG.py*, change the script exectuable in the *comment* variable to fit organizational or application need.
- To test code in the Python terminal, import the function you are testing from *AlgoG*, *choice_transaction* for transfer, *request_funds* for the charge function, and *algo_switch* for the Algogenous smart contract. It is reccomended to add a *reciever_address* and *reciever_mnemonic* in the *AlgoG* file for code that is being tested in the terminal to avoid potential errors associated with a copy-paste method. Once this is done, import the *fund_address*, *fund_mnemonic*, *receiver_address*, *receiver_mnemonic*, and *asset_id* variables from *AlgoG*. Then, run the function with the appropriate inputs as described in the *AlgoG* file.


# License
Copyright Fortior Blockchain, LLLP 2021

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
