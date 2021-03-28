import gym
import os
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.initializers import glorot_normal

# 나중에 환경이 완성되면 이것을 사용
#from env import *
#Env(True)

gamma = 0.95
epsilon = 1

env = gym.make('CartPole-v1')

memory = deque()

# 네트워크 생성, 컴파일
model = Sequential()
model.add(Dense(32, input_dim=4, kernel_initializer=glorot_normal(), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(2, activation='linear'))
model.compile(loss='mse', optimizer=Adam(lr=0.0005))
if os.path.isfile("save.h5"):
    model.load_weights("save.h5")

for episodeNumber in range(500):
    state = env.reset()
    state = np.reshape(state, [1, 4])

    maxFrame = 0

    done = False
    for frameCounter in range(500):
        env.render()

        if np.random.rand() <= epsilon:
            action = random.randrange(2)
        else :
            action = np.argmax(model.predict(state)[0])

        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, 4])

        memory.append((state, action, reward, next_state, done))

        state = next_state

        maxFrame = frameCounter

        if done == True:
            break

    print("에피소드", episodeNumber, ": ", maxFrame)

    # replay memory
    while len(memory) >= 512:
        random.shuffle(memory)

        for i in range(64):
            state, action, reward, next_state, done = memory.pop()
            target = reward
            if not done:
                target = reward + gamma * np.amax(model.predict(next_state)[0])
            target_f = model.predict(state)
            target_f[0][action] = target

            model.fit(state, target_f, epochs=1, verbose=0) # gradient 자동 계산(매우 느림) -> 나중에 개선

        if len(memory) < 1024:
            break
    
    # 랜덤으로 선택할 확률(e-greedy)
    epsilon *= 0.997
    if epsilon < 0.05:
        epsilon = 0.05

    # 때때로 파일로 저장
    if episodeNumber % 10 == 9:
        model.save("save.h5")
