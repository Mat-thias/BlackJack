This is a project to simulate a blackjack game with python on the command line.

The project was based on this tutorial: 
https://youtube.com/playlist?list=PL-0yYEHqPWkAtFOXhOwRujeJ1LoCJsw8t

NOTE: This is still under development.

The algorithm of the game is:
When a game starts, a table is created with its shoe, the dealer, a list of players.
The first serve is done, a pair of cards to the players and a single card to the dealer.
Check for any of the player has a blackjack and pay him/her out immediately.
Let the rest of the player decide their moves.
After all players who have not burst, or surrender are standing, let the dealer draw till 17 or more.
Then pay all active players; Payment could negative for loses.
    
NOTE:
    This doesn't currently support split and insurance.
    The stake isn't set manually and always fixed at 100 units.
    The project is under development.