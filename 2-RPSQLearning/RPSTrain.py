# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import random
import math
import os



#------------------------------------------------------------
# 변수 설정
#------------------------------------------------------------

rules = {0: 1, 1: 2, 2: 0}

RPS_PLAYER1 = 1
RPS_PLAYER2 = 2
PLAYER1_SCORE = 0
PLAYER2_SCORE = 0
MAX_SCORE = 5

nbActions = 3 # rock/scissors/paper
nbStates = nbActions
hiddenSize = 100
maxMemory = 500
batchSize = 50
epoch = 10
epsilonStart = 1
epsilonDiscount = 0.999
epsilonMinimumValue = 0.1
discount = 0.9
learningRate = 0.2
winReward = 1
#------------------------------------------------------------



#------------------------------------------------------------
# 가설 설정
#------------------------------------------------------------
X = tf.placeholder(tf.float32, [None, nbStates])
W1 = tf.Variable(tf.truncated_normal([nbStates, hiddenSize], stddev = 1.0 / math.sqrt(float(nbStates))))
b1 = tf.Variable(tf.truncated_normal([hiddenSize], stddev = 0.01))
input_layer = tf.nn.relu(tf.matmul(X, W1) + b1)

W2 = tf.Variable(tf.truncated_normal([hiddenSize, hiddenSize], stddev = 1.0 / math.sqrt(float(hiddenSize))))
b2 = tf.Variable(tf.truncated_normal([hiddenSize], stddev = 0.01))
hidden_layer = tf.nn.relu(tf.matmul(input_layer, W2) + b2)

W3 = tf.Variable(tf.truncated_normal([hiddenSize, nbActions], stddev = 1.0 / math.sqrt(float(hiddenSize))))
b3 = tf.Variable(tf.truncated_normal([nbActions], stddev = 0.01))
output_layer = tf.matmul(hidden_layer, W3) + b3

Y = tf.placeholder(tf.float32, [None, nbActions])
cost = tf.reduce_sum(tf.square(Y - output_layer)) / (2 * batchSize)
optimizer = tf.train.GradientDescentOptimizer(learningRate).minimize(cost)
#------------------------------------------------------------



#------------------------------------------------------------
# 랜덤값 구함
#------------------------------------------------------------
def randf(s, e):
	return (float(random.randrange(0, (e - s) * 9999)) / 10000) + s
#------------------------------------------------------------



#------------------------------------------------------------
# 가위바위보 환경 클래스
#------------------------------------------------------------
class RPSEnvironment():

	#--------------------------------
	# 초기화
	#--------------------------------
	def __init__(self):
		self.nbStates = nbActions
		self.state = np.zeros(self.nbStates, dtype = np.uint8)
		self.PLAYER1_SCORE = PLAYER1_SCORE
		self.PLAYER2_SCORE = PLAYER2_SCORE
		self.PLAYER1_PREVIOUS = None
		self.PLAYER1_RSP = None
		self.PLAYER2_PREVIOUS = None

	#--------------------------------
	# 리셋
	#--------------------------------
	def reset(self):
		self.state = np.zeros(self.nbStates, dtype = np.uint8)

	#--------------------------------
	# 현재 상태 구함
	#--------------------------------
	def getState(self):
		return np.reshape(self.state, (1, self.nbStates))



	#--------------------------------
	# 플레이어가 바뀐 현재 상태 구함
	#--------------------------------
	def getStateInverse(self):
		tempState = self.state.copy()
		
		for i in range(self.nbStates):
			if tempState[i] == RPS_PLAYER1 :
				tempState[i] = RPS_PLAYER2
			elif tempState[i] == RPS_PLAYER2 :
				tempState[i] = RPS_PLAYER1
		
		return np.reshape(tempState, (1, self.nbStates))

	#--------------------------------
	# 게임오버 검사
	#--------------------------------
	def isGameOver(self, player):
		if player == RPS_PLAYER1:
			if self.PLAYER1_SCORE >= 5:
				self.PLAYER1_SCORE = 0
				self.PLAYER2_SCORE = 0
				return True, winReward
			else:
				return False, 0
		elif player == RPS_PLAYER2:
			if self.PLAYER2_SCORE >= 5:
				self.PLAYER1_SCORE = 0
				self.PLAYER2_SCORE = 0
				return True, winReward
			else:
				return False, 0
		else:
			return False, 0

	#--------------------------------
	# 상태 업데이트
	#--------------------------------
	def updateState(self, player, action):
		self.state[action] += 1

		# print(player, " state: ", self.state)

	#--------------------------------
	# 행동 수행
	#--------------------------------
	def act(self, player, action):

		reward_add = 0
		# print("Player1_Previous: ", self.PLAYER1_PREVIOUS)
		# print("Player2_Previous: ", self.PLAYER1_PREVIOUS)
		if player == RPS_PLAYER1:

			if self.PLAYER1_PREVIOUS == None:
				self.PLAYER1_PREVIOUS = action
			else:
				self.PLAYER1_RSP = action
		elif player == RPS_PLAYER2:

			if self.PLAYER2_PREVIOUS == None:
				self.PLAYER2_PREVIOUS = action
			else:
				if rules[self.PLAYER1_RSP] == action:
					if action == self.PLAYER2_PREVIOUS:
						self.PLAYER2_SCORE += 2
						self.PLAYER1_PREVIOUS = None
						self.PLAYER2_PREVIOUS = None
						reward_add += 0.05
						self.updateState(player, action)
					else:
						self.PLAYER2_SCORE += 1
						self.PLAYER1_PREVIOUS = None
						self.PLAYER2_PREVIOUS = None
						self.updateState(player, action)
				elif rules[action] == self.PLAYER1_RSP:
					if self.PLAYER1_RSP == self.PLAYER1_PREVIOUS:
						self.PLAYER1_SCORE += 2
						self.PLAYER1_PREVIOUS = None
						self.PLAYER2_PREVIOUS = None
						self.updateState(RPS_PLAYER1, self.PLAYER1_RSP)
					else:
						self.PLAYER1_SCORE += 1
						self.PLAYER1_PREVIOUS = None
						self.PLAYER2_PREVIOUS = None
						self.updateState(RPS_PLAYER1, self.PLAYER1_RSP)

				# print(self.PLAYER1_RSP, ": ", action)

		gameOver, reward = self.isGameOver(player)

		if reward == 0:
			reward += reward_add

		if player == RPS_PLAYER1:
			nextState = self.getState()
		else:
			nextState = self.getStateInverse()

		return nextState, reward, gameOver


	#--------------------------------
	# 행동 구함
	#--------------------------------
	def getAction(self, sess, currentState):
		q = sess.run(output_layer, feed_dict = {X: currentState})
		
		while True:
			action = q.argmax()
			return action

	#--------------------------------
	# 랜덤 행동 구함
	#--------------------------------
	def getActionRandom(self):
		while True:
			action = random.randrange(0, nbActions)
			return action

#------------------------------------------------------------

#------------------------------------------------------------
# 리플레이 메모리 클래스
#------------------------------------------------------------
class ReplayMemory:

	#--------------------------------
	# 초기화
	#--------------------------------
	def __init__(self, maxMemory, discount):
		self.maxMemory = maxMemory
		self.discount = discount
		self.nbStates = nbActions

		self.inputState = np.empty((self.maxMemory, self.nbStates), dtype = np.uint8)
		self.actions = np.zeros(self.maxMemory, dtype = np.uint8)
		self.nextState = np.empty((self.maxMemory, self.nbStates), dtype = np.uint8)
		self.gameOver = np.empty(self.maxMemory, dtype = np.bool)
		self.rewards = np.empty(self.maxMemory, dtype = np.int8)
		self.count = 0
		self.current = 0



	#--------------------------------
	# 결과 기억
	#--------------------------------
	def remember(self, currentState, action, reward, nextState, gameOver):
		self.actions[self.current] = action
		self.rewards[self.current] = reward
		self.inputState[self.current, ...] = currentState
		self.nextState[self.current, ...] = nextState
		self.gameOver[self.current] = gameOver
		self.count = max(self.count, self.current + 1)
		self.current = (self.current + 1) % self.maxMemory



	#--------------------------------
	# 배치 구함
	#--------------------------------
	def getBatch(self, model, batchSize, nbActions, nbStates, sess, X):
		memoryLength = self.count
		chosenBatchSize = min(batchSize, memoryLength)
		
		inputs = np.zeros((chosenBatchSize, nbStates))
		targets = np.zeros((chosenBatchSize, nbActions))

		for i in range(chosenBatchSize):
			randomIndex = random.randrange(0, memoryLength)
			current_inputState = np.reshape(self.inputState[randomIndex], (1, nbStates))

			target = sess.run(model, feed_dict = {X: current_inputState})

			current_nextState = np.reshape(self.nextState[randomIndex], (1, nbStates))
			current_outputs = sess.run(model, feed_dict = {X: current_nextState})

			nextStateMaxQ = np.amax(current_outputs)

			if nextStateMaxQ > winReward:
				nextStateMaxQ = winReward
			
			if self.gameOver[randomIndex] == True:
				target[0, [self.actions[randomIndex]]] = self.rewards[randomIndex]
			else:
				target[0, [self.actions[randomIndex]]] = self.rewards[randomIndex] + self.discount * nextStateMaxQ

			inputs[i] = current_inputState
			targets[i] = target

		return inputs, targets
#------------------------------------------------------------

#------------------------------------------------------------
# 게임 플레이 함수
#------------------------------------------------------------
def playGame(env, memory, sess, saver, epsilon, iteration):

	#--------------------------------
	# 게임 반복
	#--------------------------------
	winCount = 0

	for i in range(epoch):
		env.reset()

		err = 0
		gameOver = False
		currentPlayer = RPS_PLAYER1
		
		while gameOver != True:
			#--------------------------------
			# 행동 수행
			#--------------------------------
			action = - 9999
			
			if currentPlayer == RPS_PLAYER1:
				currentState = env.getState()
			else:
				currentState = env.getStateInverse()

			if randf(0, 1) <= epsilon:
				action = env.getActionRandom()
			# if random.randint(0, 1) <= 0.4:
			# 	action = env.getActionRandom()
			else:
				action = env.getAction(sess, currentState)

			if epsilon > epsilonMinimumValue:
				epsilon = epsilon * epsilonDiscount
			
			nextState, reward, gameOver = env.act(currentPlayer, action)

			if reward == 1 and currentPlayer == RPS_PLAYER2:
				winCount = winCount + 1

			#--------------------------------
			# 학습 수행
			#--------------------------------
			memory.remember(currentState, action, reward, nextState, gameOver)

			inputs, targets = memory.getBatch(output_layer, batchSize, nbActions, nbStates, sess, X)
			
			_, loss = sess.run([optimizer, cost], feed_dict = {X: inputs, Y: targets})
			err = err + loss
			
			if currentPlayer == RPS_PLAYER1:
				currentPlayer = RPS_PLAYER2
			else:
				currentPlayer = RPS_PLAYER1

		print("Epoch " + str(iteration) + str(i) + ": err = " + str(err) + ": Win count = " + str(winCount) )
		# print("-----------------------------------------------")
		# print(targets)
		# print("-----------------------------------------------")

		if( (i % 10 == 0) and (i != 0) ):
			save_path = saver.save(sess, os.getcwd() + "/Model/RPSModel-1000.ckpt")
			print("Model saved in file: %s" % save_path)

	save_path = saver.save(sess, os.getcwd() + "/Model/RPSModel-1000.ckpt")
	print("Model saved in file: %s" % save_path)
#------------------------------------------------------------

#------------------------------------------------------------
# 메인 함수
#------------------------------------------------------------
def main(_):

	print("Training new model")

	# 환경 인스턴스 생성
	env = RPSEnvironment()

	# 리플레이 메모리 인스턴스 생성
	memory = ReplayMemory(maxMemory, discount)

	# 텐서플로우 초기화
	sess = tf.Session()
	sess.run(tf.global_variables_initializer())

	# 세이브 설정
	saver = tf.train.Saver()

	# # 모델 로드
	if os.path.isfile(os.getcwd() + "/Model/RPSModel-1000.ckpt.index") == True:
		saver.restore(sess, os.getcwd() + "/Model/RPSModel-1000.ckpt")
		print('Saved model is loaded!')
	
	# 게임 플레이
	iteration = 0
	while iteration < 100:
		playGame(env, memory, sess, saver, epsilonStart, iteration);
		iteration += 1

	# 세션 종료
	sess.close()
#------------------------------------------------------------

#------------------------------------------------------------
# 메인 함수 실행
#------------------------------------------------------------
if __name__ == '__main__':
	tf.app.run()
#------------------------------------------------------------
















