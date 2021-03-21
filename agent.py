import gym
import os
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# 나중에 환경이 완성되면 이것을 사용
#from env import *
#Env(True)

gamma = 0.95

epsilon = 1.0

env = gym.make('CartPole-v1')

memory = deque(maxlen=1024)

# create Network
model = Sequential()
model.add(Dense(64, input_dim=4, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(2, activation='linear'))
model.compile(loss='mse', optimizer=Adam(lr=0.002))
if os.path.isfile("save.chkpt"):
    model.load_weights("save.chkpt")

for episodeNumber in range(500):
    state = env.reset()
    state = np.reshape(state, [1, 4])

    done = False
    for frameCounter in range(500):
        env.render()

        if np.random.rand() <= epsilon:
            action = random.randrange(4)
        action = np.argmax(model.predict(state)[0])

        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, 4])

        memory.append((state, action, reward, next_state, done))

        state = next_state

        if done == True:
            break

    # 저장된 데이터로부터 학습(복기)
    if len(memory) >= 64:
        sample = random.sample(memory, 64)
        for state, action, reward, next_state, done in sample:
            target = reward
            if not done:
                target = reward + gamma * np.amax(model.predict(next_state)[0])
            target_f = model.predict(state)
            target_f[0][action] = target
            model.fit(state, target_f, epochs=1, verbose=0)

    # 랜덤으로 선택할 확률(e-greedy)
    epsilon *= 0.995
    if epsilon < 0.02:
        epsilon = 0.02

    # 때때로 파일로 저장
    if episodeNumber % 10 == 9:
        model.save("save.chkpt")
