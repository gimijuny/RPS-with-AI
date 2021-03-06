# -*- coding: utf-8 -*-

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from keras import backend as K
from rps_environment import RPS
import random

EPISODES = 1000
rules = {0: 1, 1: 2, 2: 0}

class A2CAgent:
    def __init__(self, state_size, action_size):
        self.render = False
        self.load_model = False
        # 상태와 행동의 크기 정의
        self.state_size = state_size
        self.action_size = action_size
        self.value_size = 1

        # 액터-크리틱 하이퍼파라미터
        self.discount_factor = 0.99
        self.actor_lr = 0.001
        self.critic_lr = 0.005

        # 정책신경망과 가치신경망 생성
        self.actor = self.build_actor()
        self.critic = self.build_critic()
        self.actor_updater = self.actor_optimizer()
        self.critic_updater = self.critic_optimizer()

        if self.load_model:
            self.actor.load_weights("./save_model/rps_actor_10000.h5")
            self.critic.load_weights("./save_model/rps_critic_10000.h5")

    # actor: 상태를 받아 각 행동의 확률을 계산
    def build_actor(self):
        actor = Sequential()
        actor.add(Dense(24, input_dim=self.state_size, activation='relu',
                        kernel_initializer='he_uniform'))
        actor.add(Dense(self.action_size, activation='softmax',
                        kernel_initializer='he_uniform'))
        actor.summary()
        return actor

    # critic: 상태를 받아서 상태의 가치를 계산
    def build_critic(self):
        critic = Sequential()
        critic.add(Dense(24, input_dim=self.state_size, activation='relu',
                         kernel_initializer='he_uniform'))
        critic.add(Dense(24, input_dim=self.state_size, activation='relu',
                         kernel_initializer='he_uniform'))
        critic.add(Dense(self.value_size, activation='linear',
                         kernel_initializer='he_uniform'))
        critic.summary()
        return critic

    # 정책신경망의 출력을 받아 확률적으로 행동을 선택
    def get_action(self, state):
        policy = self.actor.predict(state, batch_size=1).flatten()
        return np.random.choice(self.action_size, 1, p=policy)[0]

    # 정책신경망을 업데이트하는 함수
    def actor_optimizer(self):
        action = K.placeholder(shape=[None, self.action_size])
        advantage = K.placeholder(shape=[None, ])

        action_prob = K.sum(action * self.actor.output, axis=1)
        cross_entropy = K.log(action_prob) * advantage
        loss = -K.sum(cross_entropy)

        optimizer = Adam(lr=self.actor_lr)
        updates = optimizer.get_updates(self.actor.trainable_weights, [], loss)
        train = K.function([self.actor.input, action, advantage], [],
                           updates=updates)
        return train

    # 가치신경망을 업데이트하는 함수
    def critic_optimizer(self):
        target = K.placeholder(shape=[None, ])

        loss = K.mean(K.square(target - self.critic.output))

        optimizer = Adam(lr=self.critic_lr)
        updates = optimizer.get_updates(self.critic.trainable_weights, [], loss)
        train = K.function([self.critic.input, target], [], updates=updates)

        return train

    # 각 타임스텝마다 정책신경망과 가치신경망을 업데이트
    def train_model(self, state, action, reward, next_state, done):
        value = self.critic.predict(state)[0]
        next_value = self.critic.predict(next_state)[0]

        act = np.zeros([1, self.action_size])
        act[0][action] = 1

        # 벨만 기대 방정식를 이용한 어드벤티지와 업데이트 타깃
        if done:
            advantage = reward - value
            target = [reward]
        else:
            advantage = (reward + self.discount_factor * next_value) - value
            target = reward + self.discount_factor * next_value

        self.actor_updater([state, act, advantage])
        self.critic_updater([state, target])


if __name__ == "__main__":
    env = RPS()

    state_size = 8
    action_size = 3

    # 액터-크리틱(A2C) 에이전트 생성
    agent = A2CAgent(state_size, action_size)

    episodes = []

    r1, r2 = 0, 0
    s1, s2 = 0, 0
    p1, p2 = 0, 0

    player1_score = 0
    player2_score = 0

    state = env.reset()
    state = np.reshape(state, [1, state_size])
    for e in range(EPISODES):
        done = False

        if agent.render:
            env.render()

        rsp1 = random.randint(0, 2)
        action1 = agent.get_action(state)
        next_state, reward, done, gameOver = env.step(action1, rsp1)
        next_state = np.reshape(next_state, [1, state_size])

        if action1 == 0:
            s1 += 1
        elif action1 == 1:
            r1 += 1
        else:
            p1 += 1

        agent.train_model(state, action1, reward, next_state, done)

        state = next_state

        while not done:
            action2 = agent.get_action(state)
            if action2 == 0:
                s2 += 1
            elif action2 == 1:
                r2 += 1
            else:
                p2 += 1
            rsp2 = random.randint(0, 2)
            next_state, reward, done, gameOver = env.step(action2, rsp2)
            next_state = np.reshape(next_state, [1, state_size])

            if rules[rsp2] == action2:
                if action1 == action2:
                    player1_score += 2
                else:
                    player1_score += 1
            elif rules[action2] == rsp2:
                if rsp1 == rsp2:
                    player2_score += 2
                else:
                    player2_score += 1

            agent.train_model(state, action2, reward, next_state, done)

            state = next_state
            if done:
                # 에피소드마다 학습 결과 출력
                episodes.append(e)
                print("episode:", e)

    # agent.actor.save_weights("./save_model/rps_actor_5000.h5")
    # agent.critic.save_weights("./save_model/rps_critic_5000.h5")

    print(s1, r1, p1, s2, r2, p2)