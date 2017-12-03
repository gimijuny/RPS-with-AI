import random

rules = {0: 1, 1: 2, 2: 0}

class RPS():
    def __init__(self):
        self.Player1_Score = 0
        self.Player2_Score = 0
        self.Player1_Previous = None
        self.Player2_Previous = None
        self.states = [0, 0]
        self.win = 0
        self.lose = 0
        self.draw = 0

    def reset(self):
        self.states = [0, 0]
        return self.states

    def setState(self, state1, state2):
        self.states = [state1, state2]
        return self.states

    def setPrevious(self, previous1, previous2):
        self.Player1_Previous = previous1
        self.Player2_Previous = previous2

    def step(self, action):
        rsp = random.randint(0,2)
        print(action, " : ", rsp)
        reward = 0

        if self.Player1_Previous == None:
            self.Player1_Previous = action
            self.Player2_Previous = rsp
            if rules[rsp] == action:
                reward = 0.5
            elif rules[action] == rsp:
                reward = -0.5

        else:
            if rules[rsp] == action:
                self.win += 1
                if action == self.Player1_Previous:
                    self.Player1_Score += 2
                    self.states[0] += 2
                    reward = 1.05
                else:
                    self.Player1_Score += 1
                    self.states[0] += 1
                    reward = 1
                self.Player1_Previous = None
                self.Player2_Previous = None
            elif rules[action] == rsp:
                self.lose += 1
                if action == self.Player1_Previous:
                    self.Player2_Score += 2
                    self.states[1] += 2
                    reward = -1.05
                else:
                    self.Player2_Score += 1
                    self.states[1] += 1
                    reward = -1
                self.Player1_Previous = None
                self.Player2_Previous = None
            else:
                reward = 0
                self.draw += 1
                done = False

        if self.Player1_Score >= 5 or self.Player2_Score >= 5:
            done = True
            self.Player1_Score = 0
            self.Player2_Score = 0
        else:
            done = False

        return self.states, reward, done