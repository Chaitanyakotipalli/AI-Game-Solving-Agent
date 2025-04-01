AI-Solving Game
Title: Defending-Zombie-Simulation.
Game Introduction:  this is single Player Game where the player has to place different elements(like sniper,shotgun,charizard,samurai,bomb) to defend the incoming zombies donot letting them to cross the lawn.
                    the game duration is generaly 60 seconds and for every 20 seconds the amount of incoming zombies increases. the zombies will also attack the elemnts.
                    for more details of working of the game refer game.txt.
                    ![Game Screenshot](images/image2.png)

Game-Playing-agent: i have created a game-solving agent for the above game which is trained on 50+ testcases to play the game which maximisises the wining probabilty.i have created different utility functions to                        take descions.
                    the agent uses different kinds of heuristics which analysis the game at each frame and tacke quick and efficent decisions to deffend the lawn.
                    for more details of working of the game-agent refer agent.txt.
                    ![Game Screenshot](images/image3.png)

feauters:1.
Single player -Mode:
this game can be played by a player manually or can be played by ai agent
          the game_settings.py file contains all the settings of gan=me like screen width,speed ,total duration etc.
          in game_settings.py agent play can be modifed :
          if agent_play =1 the ai solving agent plays the game 
            agent_play =0 it allows us to play the game manually.

        2.Graphical User Interface:

The game features a user-friendly graphical interface developed using the Pygame library.
        the assets.py contains all the gif files frame for smooth movement of zombiies guns,bombs etc to get more realisitic experencies.
        we can enhance the zombies appearence
        3.legal moves:
        we can place the guns oly in a the 5*5  green lawn .
Game Rules:
1.The inital state is 
 ![Game Screenshot](images/image1.png)
 2.the game duration is generaly 60 seconds the player has to defend the lawn not allowing the zombies to cross the lawn he can use the elemnts to defend the lawn.
 if the zombie breaches the lawn game over.
  3.legal moves:
        we can place the guns only in  the 5*5  green lawn .

  4.controls we have to select the gun from the selection bar and place it in the lawn 
  the score is displayed has home zombiesyou killed till now.


  Installation :
  git clone https://github.com/Chaitanyakotipalli/AI_Game_Solving_Agent.git
  cd AI_Game_Solving_Agent

  Install 
  pip install pygame
  run the game
  python main_game.py
📌 Future Enhancements

Integrate Reinforcement Learning to improve AI adaptability.
Train the Model on more testcase and increase the game environment
Improve UI/UX with interactive elements.

Implement real-time gameplay analytics.
        
        
        
