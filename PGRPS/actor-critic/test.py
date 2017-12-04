from rps_environment import RPS
from agent1 import A2CAgent as Agent1
from agent2 import A2CAgent as Agent2

rules = {0: 1, 1: 2, 2: 0}

if __name__ == "__main__":
    agent1 = Agent1(2, 3)
    agent2 = Agent2(2, 3)
    win = 0
    lose = 0
    draw = 0
    n = 0
    print(agent1, agent2)
    while n < 1000:
        action1_previous = agent1.submitCard(None, None)
        action2_previous = agent2.submitCard(None, None)
        done = False
        print(action1_previous, action2_previous)
        while not done:
            action1_card = agent1.submitCard(action1_previous, action2_previous)
            action2_card = agent1.submitCard(action2_previous, action1_previous)

            if rules[action2_card] == action1_card:
                win += 1
                done = True
            elif rules[action1_card] == action2_card:
                lose += 1
                done = True
            else:
                draw += 1

        n += 1
    print(win, lose, draw)