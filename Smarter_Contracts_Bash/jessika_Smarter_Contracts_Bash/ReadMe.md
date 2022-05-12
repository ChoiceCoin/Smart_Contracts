<p align="center">
  <a href="" rel="noopener">
 <img src="https://avatars.githubusercontent.com/u/87402354?v=4" alt="Project logo"></a>
</p>
<h2 align="center">THE PRICE IS RIGHT</h2>

<div align="center">


</div>

---

<p align="center"> This is a guessing game with a wager
    <br> 
</p>

## 🖼 OVERVIEW
- The Price Is Right is a console game which allows a player to either gain or lose funds.
- The player has 6 trials to guess the right number
- If the player manages to guess the right number within his/her 6 trials the player gets the wager chosen by he/her transferred to their wallet.
- But if the player doesn't get the right guess in 6 trials the player loses the wager and the wager is transferred from his wallet to the creators wallet

### ⚧ Proof Of Fairness
If you look at the `game.py` file you'll see on line 113 
`winning_number = r.randint(1,100)`
This is where the random number is been chosen from 1 to 100 and if the user guesses it right he gets the award.

### ❗️ NOTE
-   The user has to have sufficent algos and sufficent amount of the asa he/her uses as a wager
- The user would have to paste his mneomic phrase and address appropriately
- This transactions happen on the TESTNET

### Requirements
- This was tested with sandbox docker
- Algorand Python SDK was used

- Choice coin can implement this inovation to increase transactions and also to increase value but there would have to be a limit to avoid the players winning all the choice coin in the creators account 😅

### 🏃🏻 RUN STEPS
 - First of all make sure you have docker and sandbox installed and running, then make sure you have the algorand python sdk installed.  
 - And finally make sure you have your virtual environment created and activated.
 - Then you can open `game.py` which is the main run file

#### 💼 FOR IMPLEMENTING THIS CODE IN CHOICE COIN
- You'll have to change the asset ID to thatof choice coin
- Change the creator address and creator mneomics 
- And thats all 

#### 🎈 FOR USING THE CODE AS A USER (THIS IS JUST FOR FUN)
 -  You'll need to have sandbox container on your docker 
 - Then you'll have to go to the `transfer.py` file call the  `asset_transfer_fund` function with the appropriate arguements and also the recievers address to have the minimum amount of Tee coin to play the game
 - Once you have sufficent algos and Teecoin on your wallet you can go ahead and and run the `game.py` file with the right inputs and test out your guessing skills
 - Check out this [video](https://youtu.be/ldXXihLD9r4) for a demo of how the game can be played 

 #### 🧌 FOR IMPLEMENTING THIS CODE AS AN ALGORAND ASSET CREATOR
 - In this I created my own asset, using the `asset_creation.py` file you can also create your own asset, just navigate to the file and follow the instructions to create your own asset.
 - You can also decide to create another address of your choice using the `create.py ` file. Check out this [video](https://www.youtube.com/watch?v=ku2hFalMWmA&t=161s) for more info on how to generate another address and pass phrase
 - Once your asset has been created it will output a link that directs you to the explorer where you can see the details of your asset. It will be adviceable to copy the asset ID and the creator address cause it would be needed to configure the game using your own asset
 - Navigate back to the game.py file and edit the `creator_address`, `creator_mnemonic ` and the `asset id` to the newly created asset and the creator address and mnemonics
 - And thats all you're good to go.


 ### ⛏️ Building Tools
 - Python
 - Algorand Python SDK
 - Sandbox Docker

### 🎉 ACKNOWLEDGEMENTS
- My discord name is jessika0

Thanks to Brian Haney AKA greenrex for putting my work to use and also Thanks to the choice coin community for being here for us I am so glad to be able to contribute to the development. LETS BUILD SOMETHING GREAT !!! 🧑‍💻



