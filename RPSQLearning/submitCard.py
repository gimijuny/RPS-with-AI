from RPSTrain import RPSEnvironment, X, W1, b1, input_layer, W2, b2, hidden_layer, W3, b3, output_layer, Y, cost, optimizer
import tensorflow as tf
import random
import sys

#------------------------------------------------------------
# 변수 설정
#------------------------------------------------------------
RPS_PLAYER1 = 1
RPS_PLAYER2 = 2
rules = {0: 1, 1: 2, 2: 0}

playerId = sys.argv[1]
card = int(sys.argv[2])
score = sys.argv[3]

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

print("playerId: ", playerId)
print("card: ", card)
print("score: ", score)
print("action: ", action)