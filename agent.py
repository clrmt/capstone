import os
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from hyperparameters import *

import gym
env = gym.make("CartPole-v1")
inputDim = 4
outputDim = 2

memory = deque(maxlen=bufferSize)

# 네트워크 생성, 컴파일
model = Sequential()
model.add(Dense(64, input_dim=inputDim, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(outputDim))
model.compile(loss='mse', optimizer=Adam(lr=learningRate))
if os.path.isfile("save.h5"):
    model.load_weights("save.h5")

for episodeNumber in range(500):
    state = env.reset()
    state = np.reshape(state, [1, inputDim])

    maxFrame = 0
    totalReward = 0

    done = False
    for frameCounter in range(500):
        env.render()

        if np.random.rand() <= epsilon:
            action = random.randrange(outputDim)
        else :
            action = np.argmax(model.predict(state)[0])

        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, inputDim])

        memory.append((state, action, reward, next_state, done))

        totalReward += reward
        state = next_state

        maxFrame = frameCounter

        if done == True:
            break

    print("에피소드", episodeNumber, ": ", maxFrame, "보상 합:", totalReward)

    # replay memory
    if len(memory) >= replaySize:
        random.shuffle(memory)

        for i in range(replaySize):
            state, action, reward, next_state, done = memory[i]
            
            target = reward
            if not done:
                target = reward + gamma * np.amax(model.predict(next_state)[0])
            target_f = model.predict(state)
            target_f[0][action] = target

            model.fit(state, target_f, epochs=1, verbose=0) # gradient 자동 계산(매우 느림) -> 나중에 개선

    # 랜덤으로 선택할 확률(e-greedy)
    epsilon *= epsilonDecay
    if epsilon < epsilonMin:
        epsilon = epsilonMin

    # 때때로 파일로 저장
    if episodeNumber % 10 == 9:
        model.save("save.h5")
