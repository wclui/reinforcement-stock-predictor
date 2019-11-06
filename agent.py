import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import keras
from keras.models import load_model
from collections import deque


EPISODES = 1000

class DQNAgent:
    def __init__(self, state_size, is_eval=False, model_name=""):
        self.state_size = state_size
        self.action_size = 3
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = load_model("models/" + model_name) if is_eval else self._build_model()
    
    def _build_model(self):
        # Sequential() creates the foundation of the layers.
        model = Sequential()
        # 'Dense' is the basic form of a neural network layer
        # Input Layer of state size(4) and Hidden Layer with 24 nodes
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        # Hidden layer with 24 nodes
        model.add(Dense(24, activation='relu'))
        # Output Layer with # of actions: 2 nodes (left, right)
        model.add(Dense(self.action_size, activation='linear'))
        # Create the model based on the information above
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * \
                    np.amax(self.model.predict(next_state)[0])

            target_f = self.model.predict(state)
            target_f[0][action] = target

            self.model.fit(state, target_f, epochs=1, verbose=0)

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    


    