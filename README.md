# black-hole

Implementation of the Black Hole board game, created in 24 hours at CopenHacks hackathon.

![GitHub Logo](/game.png)

You can play against other people online and against bots. A ranking system is also implemented so you can match yourself against others.

* http://copenhacks.com/
* https://boardgamegeek.com/boardgame/146067/black-hole
* https://www.youtube.com/watch?v=zMLE7a3faI4


#Rules

Black Hole, initially designed as a paper-and-pencil game, is played on a triangular board of 21 cells. Two players alternate turns placing a numbered disc of their color onto an empty space. Discs are numbered 1-10 and must be placed in numerical order. When all the discs have been placed, the game ends. The one board space that remains empty is the "Black Hole"; each player sums the values of his discs surrounding the Black Hole, and the player with the lower sum wins.

#Instructions to run
* create a virtualenv
  * virtalenv env
'* activate the virtual environment
  * source env/bin/activate
* use pip to install dependencies
  * pip install -r requirements.txt
* run run.py
  * python run.py
* open you webbrowser and enter http://127.0.0.1:5000
