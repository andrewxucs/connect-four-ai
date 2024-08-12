import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import random
from collections import deque
from ConnectFour import ConnectFour

class DQNAgent:
    def __init__(self):
        self.state_size = 6 * 7
        self.action_size = 7
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
    
    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state, legal_actions):
        if np.random.rand() <= self.epsilon:
            return random.choice(legal_actions)
        act_values = self.model.predict(state)
        return legal_actions[np.argmax([act_values[0][a] for a in legal_actions])]
    
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def load(self, name):
        self.model.load_weights(name)
    
    def save(self, name):
        self.model.save_weights(name + ".weights.h5")

# Training the agent
if __name__ == "__main__":
    env = ConnectFour()
    agent = DQNAgent()
    episodes = 1000
    batch_size = 32
    
    for e in range(episodes):
        state = env.create_board().flatten().reshape(1, -1)
        done = False
        player = 1
        
        while not done:
            legal_actions = env.legal_actions()
            action = agent.act(state, legal_actions)
            next_state, reward, done = env.step(action, player)
            next_state = next_state.flatten().reshape(1, -1)
            
            if done:
                if reward == 1:  # Winning move
                    reward = 1
                elif reward == 0:  # Losing move
                    reward = -1
            
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            player = 1 if player == 2 else 2  # Switch player
            
            if done:
                print(f"Episode {e+1}/{episodes}, e: {agent.epsilon:.2}")
                break
            
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        
        if e % 50 == 0:
            agent.save(f"connect_four_dqn_{e}")
            