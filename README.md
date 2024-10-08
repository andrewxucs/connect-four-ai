<img src="https://github.com/user-attachments/assets/6342c6e7-379c-48a3-9785-ce0a20d95334" alt="Connect Four AI" width="200" height="200">

# Overview
This project implements the Deep Q-Learning algorithm to play connect four.

# Instructions
Execute DQNAgent.py if you wish to train the model. The model would be stored in a file named connect_four_dqn_{e}.weights.h5, where e is the current episode number. Currently, ConnectFourMain.py is an interface that allows the user to play both sides. To play against the AI, load the model and automate one side by altering the code of ConnectFourMain.py

# Interface
The user determines whether or not s/he goes first in the console.\
The player that goes first uses the red pieces and the next player uses the blue pieces.\
To add a piece, simply click on the appropriate column.

# Credits
This project would not be possible without the open-source library PyGame.\
Deep Q-Learning was developed by researchers at Google DeepMind. Their findings were published in the following research paper:\
Link: https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf
