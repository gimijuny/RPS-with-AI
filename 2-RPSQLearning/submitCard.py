from RPSTrain import RPSEnvironment, X, W1, b1, input_layer, W2, b2, hidden_layer, W3, b3, output_layer, Y, cost, optimizer
import tensorflow as tf
import random
import sys
import os

#------------------------------------------------------------
# 변수 설정
#------------------------------------------------------------
RPS_PLAYER1 = 1
RPS_PLAYER2 = 2
rules = {0: 1, 1: 2, 2: 0}

if sys.argv[1] != None:
	playerId = sys.argv[1]
if sys.argv[2] != None:
	card1 = int(sys.argv[2])
if sys.argv[3] != "null":
	card2 = int(sys.argv[3])
else:
	card2 = None
if sys.argv[4] != None:
	player_score = int(sys.argv[4])
if sys.argv[5] != None:
	ai_score = int(sys.argv[5])

#------------------------------------------------------------
# 게임 플레이 함수
#------------------------------------------------------------
def playGame(env, sess):
	currentPlayer = RPS_PLAYER1

	env.PLAYER1_SCORE = ai_score
	env.PLAYER2_SCORE = player_score

	env.updateState(RPS_PLAYER1)

	if currentPlayer == RPS_PLAYER1:
		currentState = env.getState()
	else:
		currentState = env.getStateInverse()

	if random.randint(0, 1) <= 0.4:
		action = env.getActionRandom()
		print("random")
	else:
		action = env.getAction(sess, currentState)

	env.act(currentPlayer, action)

	if currentPlayer == RPS_PLAYER1:
		currentPlayer = RPS_PLAYER2
	else:
		currentPlayer = RPS_PLAYER1

	if card2 != None:
		env.act(currentPlayer, card2)
	else:
		env.act(currentPlayer, card1)

	print("playerId: ", playerId)
	print("card1: ", card1)
	print("card2: ", card2)
	print("Player_Score: ", player_score)
	print("AI_Score: ", ai_score)
	print("action: ", action)

# ------------------------------------------------------------
# 메인 함수
# ------------------------------------------------------------
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

# ------------------------------------------------------------

# ------------------------------------------------------------
# 메인 함수 실행
# ------------------------------------------------------------
if __name__ == '__main__':
	tf.app.run()
# ------------------------------------------------------------

