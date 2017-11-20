# -*- coding: utf-8 -*-

from RPSTrain import RPSEnvironment, X, W1, b1, input_layer, W2, b2, hidden_layer, W3, b3, output_layer, Y, cost, optimizer
import tensorflow as tf
import os
import random
import math

#------------------------------------------------------------
# 변수 설정
#------------------------------------------------------------
RPS_PLAYER1 = 1
RPS_PLAYER2 = 2
rules = {0: 1, 1: 2, 2: 0}

#------------------------------------------------------------

#------------------------------------------------------------
# 게임 플레이 함수
#------------------------------------------------------------
def playGame(env, sess):

	env.reset()

	gameOver = False
	currentPlayer = RPS_PLAYER1

	player_score = 0
	ai_score = 0

	while gameOver != True:
		action = - 9999
		
		if currentPlayer == RPS_PLAYER1:
			currentState = env.getState()
		else:
			currentState = env.getStateInverse()

		if random.randint(0, 1) <= 0.4:
			action = env.getActionRandom()
		else:
			action = env.getAction(sess, currentState)

		env.act(currentPlayer, action)

		player = input("Enter your choice (R/P/S): ")
		player = player.upper()

		while player != "R" and player != "P" and player != "S":
			player = input("Enter your choice (R/P/S): ")
			player = player.upper()

		if player == "R":
			RSP = 1
		elif player == "P":
			RSP = 2
		elif player == "S":
			RSP = 0

		if action == 0:
			print("AI choice: S")
		elif action == 1:
			print("AI choice: R")
		elif action == 2:
			print("AI choice: P")

		currentState = env.getStateInverse()
		env.act(RPS_PLAYER2, RSP)

		print(env.PLAYER1_SCORE)
		print(env.PLAYER2_SCORE)

		if rules[action] == RSP:
			player_score += 1
			print("Player Win")
			print(player_score, " : ", ai_score)
		elif rules[RSP] == action:
			ai_score += 1
			print("AI Win")
			print(player_score, " : ", ai_score)
		else:
			print("It's tie")

		if player_score >= 3:
			gameOver = True
			print("Game Over!! Player Winner")
		elif ai_score >= 3:
			gameOver = True
			print("Game Over!! Player Winner")

#------------------------------------------------------------

#------------------------------------------------------------
# 메인 함수
#------------------------------------------------------------
def main(_):

	# 환경 인스턴스 생성
	env = RPSEnvironment()

	# 텐서플로우 초기화
	sess = tf.Session()
	sess.run(tf.global_variables_initializer())

	# 세이브 설정
	saver = tf.train.Saver()

	# 모델 로드
	if os.path.isfile(os.getcwd() + "/RPSModel.ckpt.index") == True:
		saver.restore(sess, os.getcwd() + "/RPSModel.ckpt")
		print('saved model is loaded!')
	
	# 게임 플레이
	playGame(env, sess)
	
	# 세션 종료
	sess.close()
#------------------------------------------------------------

#------------------------------------------------------------
# 메인 함수 실행
#------------------------------------------------------------
if __name__ == '__main__':
	tf.app.run()
#------------------------------------------------------------

