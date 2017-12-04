import random

rules = {0: 1, 1: 2, 2: 0}

class RPS():
    def __init__(self):
        self.Player1_Score = 0
        self.Player2_Score = 0
        self.states = [0, 0]
        self.win = 0
        self.lose = 0
        self.draw = 0

    def reset(self):
        self.states[0] = 0
        self.states[1] = 0
        return self.states

    def setState(self, state1, state2):
        self.states = [state1, state2]
        return self.states

    def step(self, action):
        rsp = random.randint(0,2)
        print(action, " : ", rsp)
        if rules[rsp] == action:
            reward = 1
            self.Player1_Score += 1
            self.states[0] += 1
            self.win += 1
            done = True
        elif rules[action] == rsp:
            reward = -1
            self.Player2_Score += 1
            self.states[1] += 1
            self.lose += 1
            done = True
        else:
            reward = 0
            self.draw += 1
            done = False

        # if self.Player1_Score >= 3 or self.Player2_Score >= 3:
        #     done = True
        # else:
        #     done = False

        return self.states, reward, done