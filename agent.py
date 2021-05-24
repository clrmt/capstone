# run_mode = 실행 모드
# 1 = 초기부터 학습
# 2 = 세이브파일로부터 이어서 학습
# 3 = 세이브파일로부터 실행 + 화면 표시
# 4 = 세이브파일로부터 실행 + 화면 비표시
run_mode = 3

print_interval = 1 # 에피소드의 print 간격
main_save_file = "save.h5" # 세이브파일 이름
stage_build_with_agent = True # Agent의 검증을 통한 스테이지 생성



import os
import random
import numpy as np
from collections import deque
from matplotlib import pyplot as plt
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from hyperparameters import *
from env import *



if stage_build_with_agent == True:
    env = Env(False, "stageBuilder")
else:
    env = Env(False, "")
inputDim = env.observationSize
outputDim = env.actionSize

memory = deque(maxlen=bufferSize)

model = Sequential()
model.add(Dense(layerNode, input_dim=inputDim, activation='relu'))
model.add(Dense(layerNode, activation='relu'))
model.add(Dense(layerNode, activation='relu'))
model.add(Dense(outputDim))
opt = tf.keras.optimizers.Adam(lr=learningRateDQN)

if run_mode >= 2:
    if os.path.isfile(main_save_file):
        model.load_weights(main_save_file)
if run_mode >= 3:
    epsilon = 0.0
    epsilonMin = 0.0
    epsilonDecay = 0.0

reward_avg = 0
reward_avgs = []

for i in range(episodeNumber):
    state = env.reset()
    state = np.reshape(state, [1, inputDim])

    maxFrame = 0
    totalReward = 0

    done = False
    
    for frameCounter in range(stepNumber):
        if run_mode == 3:
            env.render()
            sleep(0.03)

        if np.random.rand() <= epsilon:
            action = random.randrange(outputDim)
        else :
            action = np.argmax(model(state)[0])

        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, inputDim])

        #print(next_state, reward)

        memory.append((state, action, reward, next_state, done))

        totalReward += reward
        state = next_state

        maxFrame = frameCounter

        if done == True:
            break
    if i == 0:
        reward_avg = totalReward
    else:
        reward_avg = reward_avg * 0.99 + totalReward * 0.01
    reward_avgs.append(reward_avg)
        
    if i % print_interval == 0:
        print("에피소드 ", i, " : ", maxFrame, ", epsilon: ", epsilon, ", 보상 합:", totalReward, sep='')
        if run_mode < 3:
            model.save(main_save_file)

    if run_mode >= 3:
        continue
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

plt.plot(reward_avgs)
plt.show()
