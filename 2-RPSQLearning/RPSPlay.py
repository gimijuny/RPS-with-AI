# -*- coding: utf-8 -*-

from RPSTrain import RPSEnvironment, X, W1, b1, input_layer, W2, b2, hidden_layer, W3, b3, output_layer, Y, cost, optimizer
import tensorflow as tf
import os
import random
import math
import test

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

	PLAYER1_PREVIOUS = None
	PLAYER2_PREVIOUS = None
	PLAYER1_Choice = None
	PLAYER2_Choice = None

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
			print("random")
		else:
			action = env.getAction(sess, currentState)

		PLAYER1_PREVIOUS = action

		env.act(currentPlayer, action)

		player = input("Enter your first choice (R/P/S): ")
		player = player.upper()

		while player != "R" and player != "P" and player != "S":
			player = input("Enter your first choice (R/P/S): ")
			player = player.upper()

		if player == "R":
			RSP = 1
		elif player == "P":
			RSP = 2
		elif player == "S":
			RSP = 0

		PLAYER2_PREVIOUS = RSP

		if action == 0:
			print("AI choice: S")
		elif action == 1:
			print("AI choice: R")
		elif action == 2:
			print("AI choice: P")

		env.act(RPS_PLAYER2, RSP)

		tie = False
		while tie != True:
			# 두번째 가위바위보
			if currentPlayer == RPS_PLAYER1:
				currentState = env.getState()
			else:
				currentState = env.getStateInverse()

			if random.randint(0, 1) <= 0.4:
				action2 = env.getActionRandom()
				print("random")
			else:
				action2 = env.getAction(sess, currentState)

			PLAYER1_Choice = action2
			env.act(currentPlayer, action2)

			player2 = input("Enter your second choice (R/P/S): ")
			player2 = player2.upper()

			while player2 != "R" and player2 != "P" and player2 != "S":
				player2 = input("Enter your second choice (R/P/S): ")
				player2 = player2.upper()

			if player2 == "R":
				RSP2 = 1
			elif player2 == "P":
				RSP2 = 2
			elif player2 == "S":
				RSP2 = 0

			PLAYER2_Choice = RSP2

			if action2 == 0:
				print("AI choice: S")
			elif action2 == 1:
				print("AI choice: R")
			elif action2 == 2:
				print("AI choice: P")

				# print("PLAYER1 Previous: ", PLAYER1_PREVIOUS)
				# print("PLAYER2 Previous: ", PLAYER2_PREVIOUS)
				# print("PLAYER1 choice: ", PLAYER1_Choice)
				# print("PLAYER2 choice: ", PLAYER2_Choice)
				# print("PLAYER2 action: ", player2)

			env.act(RPS_PLAYER2, RSP2)

			if rules[PLAYER2_Choice] == PLAYER1_Choice:
				if PLAYER1_Choice == PLAYER1_PREVIOUS:
					ai_score += 2
					tie = True
					print("AI Win")
				else:
					ai_score += 1
					tie = True
					print("AI Win")
			elif rules[PLAYER1_Choice] == PLAYER2_Choice:
				if PLAYER2_Choice == PLAYER2_PREVIOUS:
					player_score += 2
					tie = True
					print("Player Win")
				else:
					player_score += 1
					tie = True
					print("Player Win")
			else:
				print("it's tie")

			# print("Player1_Score: ", env.PLAYER1_SCORE)
			# print("Player2_Score: ", env.PLAYER2_SCORE)

			print("AI Score: ", ai_score)
			print("Player Score:", player_score)

			if player_score >= 5:
				gameOver = True
				print("Game Over!! Player Winner")

			elif ai_score >= 5:
				gameOver = True
				print("Game Over!! ai Winner")

			print("----------------------------------------------")
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
	if os.path.isfile(os.getcwd() + "/RPSModel2.ckpt.index") == True:
		saver.restore(sess, os.getcwd() + "/RPSModel2.ckpt")
		print('saved model is loaded!')
	
	# 게임 플레이
	playGame(env, sess)
	
	# 세션 종료
	sess.close()
#------------------------------------------------------------

def submitCard(playerId, card, score):
	# 환경 인스턴스 생성
	env = RPSEnvironment()
	env.reset()

	# 텐서플로우 초기화
	sess = tf.Session()
	sess.run(tf.global_variables_initializer())

	currentPlayer = RPS_PLAYER1

	if currentPlayer == RPS_PLAYER1:
		currentState = env.getState()
	else:
		currentState = env.getStateInverse()

	if random.randint(0, 1) <= 0.4:
		action = env.getActionRandom()
	else:
		action = env.getAction(sess, currentState)

	env.act(currentPlayer, action)
	env.act(RPS_PLAYER2, card)

	return action

def submitMatch(playerId, match):

	print(playerId, match)
#------------------------------------------------------------
# 메인 함수 실행
#------------------------------------------------------------
if __name__ == '__main__':
	tf.app.run()
#------------------------------------------------------------

