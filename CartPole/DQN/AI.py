import tensorflow as tf
import random
import numpy as np
import gym
from collections import deque

epsilon = 0.5
REPLAY_SIZE = 10000
BATCH_SIZE = 32

class AI:
    def __init__(self, env):
        self.env = env
        self.create_DQN()
        self.create_train()
        self.replay = deque()
        tf.InteractiveSession().run(tf.initialize_all_variables())

    def create_DQN(self):
        self.state_ph = tf.placeholder(tf.float32, [None, 4])
        W1 = self.weight_variable([4, 20])
        b1 = self.bias_variable([20])
        W2 = self.weight_variable([20, 2])
        b2 = self.bias_variable([2])
        hidden_layer = tf.nn.relu(tf.matmul(self.state_ph, W1) + b1)
        self.Q = tf.matmul(hidden_layer, W2) + b2

    def weight_variable(self,shape):
        initial = tf.truncated_normal(shape)
        return tf.Variable(initial)

    def bias_variable(self,shape):
        initial = tf.constant(0.01, shape = shape)
        return tf.Variable(initial)

    def egreedy_action(self, state):
        if random.random() < epsilon:
            return 1 if random.random() > 0.5 else 0
        Q_value = self.Q.eval(feed_dict = {self.state_ph:[state]})[0]
        return np.argmax(Q_value)

    def greedy_action(self, state):
        return np.argmax(self.Q.eval(feed_dict = {self.state_ph:[state]})[0])

    def create_train(self):
        self.y_ph = tf.placeholder(tf.float32, [None])
        self.action_ph = tf.placeholder(tf.float32, [None, 2])
        batch_Q = tf.reduce_sum(self.Q * self.action_ph, reduction_indices = 1)
        loss = tf.reduce_mean(tf.square(batch_Q - self.y_ph))
        self.optimizer = tf.train.AdamOptimizer(0.0001).minimize(loss)


    def update(self, state, action, reward, new_state, done):
        y = 0
        if done:
            y = reward
        else:
            y = reward + 0.9*np.max(self.Q.eval(feed_dict = {self.state_ph:[new_state]})[0])

        a = [0, 0]
        a[action] = 1
        self.replay.append((state, a, y))
        if len(self.replay) > REPLAY_SIZE:
            self.replay.popleft()
        if len(self.replay) > BATCH_SIZE:
            self.train()

    def train(self):
        batch = random.sample(self.replay, BATCH_SIZE)
        states = [data[0] for data in batch]
        actions = [data[1] for data in batch]
        ys = [data[2] for data in batch]
        self.optimizer.run(feed_dict = {
            self.y_ph : ys,
            self.action_ph : actions,
            self.state_ph : states
        })


        

