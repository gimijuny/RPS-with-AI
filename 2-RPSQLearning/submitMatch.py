from RPSTrain import RPSEnvironment, X, W1, b1, input_layer, W2, b2, hidden_layer, W3, b3, output_layer, Y, cost, optimizer
import tensorflow as tf
import sys

#------------------------------------------------------------
# 변수 설정
#------------------------------------------------------------
RPS_PLAYER1 = 1
RPS_PLAYER2 = 2
rules = {0: 1, 1: 2, 2: 0}

# 환경 인스턴스 생성
env = RPSEnvironment()
env.reset()

# 텐서플로우 테스트
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))

a = tf.constant(10)
b = tf.constant(32)
print(sess.run(a+b))

# 텐서플로우 초기화
sess = tf.Session()
sess.run(tf.global_variables_initializer())

playerId = sys.argv[1]
match = sys.argv[2]

print("playerId: ", playerId)
print("match: ", match)