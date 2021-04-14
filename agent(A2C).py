import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras import layers
from hyperparameters import *



from env import *
env = Env(False)








def getModel(obsNumber, actionNumber):
  inputs = layers.Input(obsNumber)
  full1 = layers.Dense(layerNode, activation="relu")(inputs)
  actor = layers.Dense(actionNumber)(full1)
  critic = layers.Dense(1)(full1)
  return tf.keras.Model(inputs = inputs, outputs = [actor, critic])
optimizer = tf.keras.optimizers.Adam(learning_rate=learningRate)

model = getModel(3, 5)
#model.load_weights("saveA2C.h5")




def env_step(action):
  state, reward, done, _ = env.step(action)
  return (np.array(state, np.float32), np.array(reward, np.int32), np.array(done, np.int32))





@tf.function
def train_step(state):

  with tf.GradientTape() as tape:



    action_probs = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
    values = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
    rewards = tf.TensorArray(dtype=tf.int32, size=0, dynamic_size=True)

    initial_state_shape = state.shape

    for t in tf.range(stepNumber):
      #env.render()
      #sleep(0.03)
      state = tf.expand_dims(state, 0)

      action_logits_t, value = model(state)

      action = tf.random.categorical(action_logits_t, 1)[0, 0]
      action_probs_t = tf.nn.softmax(action_logits_t)

      state, reward, done = tf.numpy_function(env_step, [action], [tf.float32, tf.int32, tf.int32])
      state.set_shape(initial_state_shape)

      action_probs = action_probs.write(t, action_probs_t[0, action])
      values = values.write(t, tf.squeeze(value))
      rewards = rewards.write(t, reward)

      if tf.cast(done, tf.bool):
        break

    action_probs = action_probs.stack()
    values = values.stack()
    rewards = rewards.stack()



    n = tf.shape(rewards)[0]
    
    returns = tf.TensorArray(dtype=tf.float32, size=n)

    rewards = tf.cast(rewards[::-1], dtype=tf.float32)
    discounted_sum = tf.constant(0.0)
    discounted_sum_shape = discounted_sum.shape
    for i in tf.range(n):
      reward = rewards[i]
      discounted_sum = reward + gamma * discounted_sum
      discounted_sum.set_shape(discounted_sum_shape)
      returns = returns.write(i, discounted_sum)
    returns = returns.stack()[::-1]

    returns = (returns - tf.math.reduce_mean(returns)) / (tf.math.reduce_std(returns) + 1e-7)



    action_probs, values, returns = [tf.expand_dims(x, 1) for x in [action_probs, values, returns]] 
    action_log_probs = tf.math.log(action_probs)
    actor_loss = -tf.math.reduce_sum(action_log_probs * (returns - values))
    critic_loss = tf.keras.losses.Huber(reduction=tf.keras.losses.Reduction.SUM)(values, returns)

    loss = actor_loss + critic_loss

  grads = tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(grads, model.trainable_variables))

  

  return tf.math.reduce_sum(rewards)









reward_avg = 0
reward_avgs = []

for i in range(episodeNumber):

  initial_state = tf.constant(env.reset(), dtype=tf.float32)
  reward_current = float(train_step(initial_state))

  if i == 0:
    reward_avg = reward_current
  else:
    reward_avg = reward_avg * 0.99 + reward_current * 0.01
  reward_avgs.append(reward_avg)
  if i % 100 == 0:
    print(i, reward_avg, reward_current)

plt.plot(reward_avgs)
plt.show()
model.save("saveA2C.h5")
