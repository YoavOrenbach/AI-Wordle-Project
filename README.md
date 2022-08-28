
# AI Wordle Project
A project that uses AI to play the Wordle game. 
This was done as a project for the Introduction to AI course at HUJI.


In this project we used a number of different methods to solve the Wordle game. These methods include:
1. Random and Total random algorithms
2. Adversarial algorithms which induce Minimax with alpha-beta pruning and Expectimax algorithms.
3. Reinforcement learning using the Q-learning algorithm.
4. Information-theory based algorithm, the entropy algorithms

We also implemented different variations of the game including:
1. Absurdle - An Adverserial version, which keeps a list of the possible secret words, and try to give the pattern that will reduce it as least as possible.
2. Noisy - One of the tiles may change with an equal probability among all the colors.
3. Yellow - The tiles can be only yellow or gray, meaning green becomes yellow.
4. Vocabulary - Change the vocabulary of the game:
    1. Fake - Each word is a random sequence of 5 letters in from the english alphabet.
    2. Real - Subset of the game vocabulary, which change the complexity of the game.

## To run the code
1. Run the command ```pip3 install -r requirements.txt```
2. Run ```python3 run_with_gui.py``` to run the game with gui.

    When running the gui you can choose any Wordle game variation (apart from Fake vocabulary since it changes the
    words for all other games) and any algorithm we used.
   
    In addition, you can choose a secret word for the algorithms to guess or randomize one 
    (except for Absurdle where there is no secret word).

3. (Optional) run ```python3 simulate_games.py``` to simulate multiple Wordle games with a pygame interface.

    You can run simulate_games.py with different arguments to simulate different game variation and different algorithms.
    Specifically, you can use the flag -n to change the number of games, -u to use the pygame interface, -g to choose a game type, -a to choose an algorithm type.
   
    For example, you can run ```python3 simulate_games.py -n 10 -u True -g Noisy-Wordle -a Q-learning ``` to simulate 10 Noisy Wordle games using the Q-learning algorithm.


### Results
The results achieved from all the different methods can be found in our report ```all_over_the_wordle_report.pdf```



## Authors
- Yoav Orenbach, yoav.orenbach@mail.huji.ac.il
- Dvir Amar, dvir.amar@mail.huji.ac.il
- Adi Rabinovitz, adi.rabinovitz@mail.huji.ac.il
- Amit Keinan, amit.keinan2@mail.huji.ac.il
