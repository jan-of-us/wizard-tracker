# Wizard Score Tracker

#### Description:

This is an app to track Scores for the 'Wizard' Cardgame.
The program is written in python and all .ui-files were created with the "Qt Designer".
The program can track games and also display a history of played games.

#### Brief explanation of the game
Wizard is a cardgame. In the first round each player gets one card, in the second round two and so on, until all the cards are distributed, which is the final round. With the card(s) each player has to predict how many tricks they might get. The sum of predictions can't be equal to the amount of tricks for the round. A card wins a trick, if it's the highest value played, a joker ("Wizard") card, or a trump card (if multiple trump cards are played the highest wins). The trump is decided by turning a card from the leftovers after giving each player their cards (final round is without trump).
After all tricks are played, each player counts their tricks. If they matched their prediction, they get points, if not they lose points.

#### General program explanation
The program starts with a main menu. From there you can either access the history or start a new game. The latter will launch a window where the players names can be entered and the amount of cards that are used can be chosen.

When all player names are given the program will launch into it's main routine. For each round the Predictions for all players can be entered. The program checks if the input is valid, and if so moves on to the results of the round. This will repeat until the game is over at which point a new window will be launched where the final results are displayed and a plot of the game history is created.

From there you can either go back to the main menu, exit the program or start another round with the same players and cards.

If History is chosen in the main menu, a new window will launch where the results of previously played games are displayed and plotted. With the dropdown menu you can change between all games in the database.
### Screenshots
#### Main Menu
![image](https://user-images.githubusercontent.com/89318982/141688102-9c71cc0e-85db-4a52-b738-4b42fce4cdd6.png)
#### Player names and card selection
![image](https://user-images.githubusercontent.com/89318982/141688108-f214193b-cae0-4b2e-abfb-5c758d1e6460.png)
#### Gameplay
![image](https://user-images.githubusercontent.com/89318982/141688111-d70a6172-9a4c-46ca-908c-b4810b74c904.png)
![image](https://user-images.githubusercontent.com/89318982/141688112-4758ce4e-3c01-4b78-8031-68a61a5259bc.png)
#### Game Ending
![image](https://user-images.githubusercontent.com/89318982/141688114-8c021fa0-d537-4133-a8df-8a7f3850eff1.png)
#### History Window
![image](https://user-images.githubusercontent.com/89318982/141688115-6edf91a2-700e-4db0-b438-bd971511994a.png)
