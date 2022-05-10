## SMART CONTRACT (Flash Loan) in Pyteal

&nbsp;

### Overview

 - The Smart Contract in the `approval_program` function handles and manages the flash loan which includes borrowing, funding the account for staking(increase/decrease) and withdraws profit after the loan has been paid. 

&nbsp;

### To use

 - `git clone` this repository

 - Activate a virtual environment by `python -m venv env`, then `pip install py-algorand-sdk`. Necessary imports have been made. 

 - Declare algod connection parameters, and mnemonics. 

&nbsp;

### Results

 - The `compileProgram` method generates TEAL code output (check `main` function), which is located in the root folder. 

