import os
import random
import numpy as np
from collections import deque
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from hyperparameters import *

from env import *
env = Env(False)
inputDim = 2
outputDim = 5

memory = deque(maxlen=bufferSize)

# 네트워크 생성, 컴파일
model = Sequential()
model.add(Dense(firstLayer, input_dim=inputDim, activation='relu'))
model.add(Dense(secondLayer, activation='relu'))
model.add(Dense(outputDim))
opt = Adam(lr=learningRate)
#model.compile(loss='mse', optimizer=Adam(lr=learningRate))

if os.path.isfile("save.h5"):
    model.load_weights("save.h5")

for episodeNumber in range(episodeNumber):
    state = env.reset()
    state = np.reshape(state, [1, inputDim])

    maxFrame = 0
    totalReward = 0

    done = False
    
    for frameCounter in range(500):
        env.render()
        sleep(0.03)

        if np.random.rand() <= epsilon:
            action = random.randrange(outputDim)
        else :
            action = np.argmax(model(state)[0])

        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, inputDim])

        memory.append((state, action, reward, next_state, done))

        totalReward += reward
        state = next_state

        maxFrame = frameCounter

        if done == True:
            break

    print("에피소드 ", episodeNumber, " : ", maxFrame, ", epsilon: ", epsilon, ", 보상 합:", totalReward, sep='')

    # replay memory
    if len(memory) >= replaySize:

        mini_batch = random.sample(memory, replaySize)

        states = np.array([sample[0][0] for sample in mini_batch])
        actions = np.array([sample[1] for sample in mini_batch])
        rewards = np.array([sample[2] for sample in mini_batch])
        next_states = np.array([sample[3][0] for sample in mini_batch])
        dones = np.array([sample[4] for sample in mini_batch])

        with tf.GradientTape() as tape:
            
            predicts = tf.reduce_sum(tf.one_hot(actions, outputDim) * model(states), axis = 1)
            targets = rewards + (1 - dones) * gamma * np.amax(model(next_states), axis = -1)
            loss = tf.reduce_mean(tf.square(targets - predicts))
            
        grads = tape.gradient(loss, model.trainable_variables)
        opt.apply_gradients(zip(grads, model.trainable_variables))

    # 랜덤으로 선택할 확률(e-greedy)
    epsilon *= epsilonDecay
    if epsilon < epsilonMin:
        epsilon = epsilonMin

    # 때때로 파일로 저장
    if episodeNumber % 20 == 9:
        model.save("save.h5")
