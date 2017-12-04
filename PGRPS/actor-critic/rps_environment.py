# -*- coding: utf-8 -*-

import random

rules = {0: 1, 1: 2, 2: 0}

class RPS():
    def __init__(self):
        self.Player1_Score = 0
        self.Player2_Score = 0
        self.Player1_Previous = None
        self.Player2_Previous = None
        self.states = [0, 0, 0, 0, 0, 0, 0, 0]
        self.win = 0
        self.lose = 0
        self.draw = 0

    def reset(self):
        self.states = [0, 0, 0, 0, 0, 0, 0, 0]
        self.Player1_Previous = None
        self.Player2_Previous = None
        self.Player1_Score = 0
        self.Player2_Score = 0
        return self.states

    def setScore(self, score1, score2):
        self.Player1_Score = score1
        self.Player2_Score = score2
        return self.states

    def setPrevious(self, previous1, previous2):
        self.Player1_Previous = previous1
        self.Player2_Previous = previous2

    def step(self, action, rsp):
        print(action, " : ", rsp)
        reward = 0

        done = False
        if self.Player1_Previous == None:
            self.Player1_Previous = action
            self.Player2_Previous = rsp
            if rules[rsp] == action:
                reward = 0.05
            elif rules[action] == rsp:
                reward = -0.05

        else:
            if rules[rsp] == action:
                done = True
                self.win += 1
                if action == self.Player1_Previous:
                    self.Player1_Score += 2
                    reward = 0.1
                else:
                    self.Player1_Score += 1
                    reward = 0.05
                self.Player1_Previous = None
                self.Player2_Previous = None
            elif rules[action] == rsp:
                done = True
                self.lose += 1
                if action == self.Player1_Previous:
                    self.Player2_Score += 2
                    reward = -0.1
                else:
                    self.Player2_Score += 1
                    reward = -0.05
                self.Player1_Previous = None
                self.Player2_Previous = None
            else:
                self.draw += 1

        gameOver = self.gameOver()

        states = list()
        if self.Player1_Previous != None:
            states.append(self.Player1_Previous)
            states.append(self.Player2_Previous)
            if rules[self.Player2_Previous] == self.Player2_Previous:
                states.append(1)
            elif rules[self.Player1_Previous] == self.Player1_Previous:
                states.append(-1)
            else:
                states.append(0)
            states.append(action)
            states.append(rsp)
            if rules[rsp] == action:
                states.append(1)
            elif rules[action] == rsp:
                states.append(-1)
            else:
                states.append(0)
        else:
            states.append(action)
            states.append(rsp)
            if rules[rsp] == action:
                states.append(1)
            elif rules[action] == rsp:
                states.append(-1)
            else:
                states.append(0)
            states.append(3)
            states.append(3)
            states.append(3)
        states.append(self.Player1_Score)
        states.append(self.Player2_Score)

        return states, reward, done, gameOver

    def gameOver(self):
        if self.Player1_Score >= 5:
            gameOver = True
            self.reset()
        elif self.Player2_Score >= 5:
            gameOver = True
            self.reset()
        else:
            gameOver = False

        return gameOver