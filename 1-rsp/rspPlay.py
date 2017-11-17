import random

choices = []
sample = [0, 1, 2]
rules = {0: 1, 1: 2, 2: 0}
rock = 0
scissor = 0
paper = 0
n = 0

# 초기값 설정
while n < 33:
    choices.append(0)
    choices.append(1)
    choices.append(2)
    rock += 1
    scissor += 1
    paper += 1
    n += 1

num = 0
# 가위바위보 학습
while num < 1000:
    opponent = random.choice(sample)
    agent = random.choice(choices)
    num += 1
    if rules[opponent] == agent:
        choices.append(agent)
    elif rules[agent] == opponent:
        choices.remove(agent)

def submitCard():
    choice = random.choice(choices)
    return choice