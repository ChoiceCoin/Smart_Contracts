### SMART CONTRACT

## Problem Statement:

Voting allows accounts to register and vote for arbitrary choices.
Here a choice is any byte slice and anyone is allowed to register to vote.
This example has a configurable registration period defined by the global state RegBegin and
RegEnd which restrict when accounts can register to vote.
There is also a separate configurable voting period defined by the global state VotingBegin and VotingEnd which
restrict when voting can take place.
An account must register in order to vote. Accounts cannot vote more than once, and if an account opts out of
the application before the voting period has concluded, their vote is discarded.
The results are visible in the global state of the application,
and the winner is the candidate with the highest number of votes.

## Requirements:

- pyteal
- Purestake API Token

### Install

- PyTeal requires Python version >= 3.6.
- cd to the directory where requirements.txt is located.
- activate your virtualenv.
- run: pip install -r requirements.txt in your shell.

### Read broadly on the Solution and Description in my Article

- https://hashnode.com/post/pyteal-voting-smart-contract-ckz1gzudw0uqq9js1cjplbnzj

### Run

- Run the python create-account.py contract in your shell

copy the generated mnemonic and paste where necessary

- Run python contract.py to generate the teal files and finally

- Run python deploy.py to deploy the smart contract
