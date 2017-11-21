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

# 환경 인스턴스 생성
env = RPSEnvironment()

# 텐서플로우 초기화
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# 세이브 설정
saver = tf.train.Saver()

# 모델 로드
if os.path.isfile(os.getcwd() + "/Model/RPSModel-1000.ckpt.index") == True:
	saver.restore(sess, os.getcwd() + "/Model/RPSModel-1000.ckpt")
	print('saved model is loaded!')

def show_me_the_card(card):
    env.act(1, card)
    currentPlayer = RPS_PLAYER2
    if currentPlayer == RPS_PLAYER1:
        currentState = env.getState()
    else:
        currentState = env.getStateInverse()

    if random.randint(0, 1) <= 0.4:
        action = env.getActionRandom()
    else:
        action = env.getAction(sess, currentState)
    env.act(currentPlayer, action)

    return action