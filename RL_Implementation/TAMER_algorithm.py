import random
import numpy as np
from numpy import array
from random import randint
from sklearn.linear_model import LinearRegression


# TODO: Do this via online learning

#####################################################################
# Initialize reinforcement model with the stepSize                  #
# Vector of states s init to 0                                      #
# s = 0                                                             #
# Vector of features f init to 0                                    #
# f = 0                                                             #
# while true:                                                       #
# h = randint(-1, 1) # TODO: Change it to come from a function      #
# h = getHumanReinfbasedOnFeatures -> random for the moment         #
# if h != 0:                                                        #
#      error = h - PredictionOfTheModelGivenFeatures(f)             #
#      UpdateReinfModel(f, error)                                   #
#   s = GetVectorOfStates                                           #
#   a = argmax(ReinfModel.predict(getFeatures(s, a)))               #
#   f = getFeatures(s, a)                                           #
#   takeAction(a)                                                   #
#   waitForNextTimestep                                             #
#####################################################################

puddle_dim = 1

#####################################################################
# is_in_puddle(min_x, max_x, min_y, max_y)
# -------------------------------------------------------------------
#####################################################################
def is_in_puddle(x, y, puddle):
    min_x = puddle[0][0]
    max_x = puddle[3][0]
    min_y = puddle[3][1]
    max_y = puddle[0][1]

    if min_x <= x <= max_x:
        if min_y <= y <= max_y:
            return True
    return False


# TODO: This can be shortened
#####################################################################
# create_puddles(pd)
# -------------------------------------------------------------------
# Description: initializes puddles
# Returns: Initialized puddles
#####################################################################
def get_puddles(pd):
    inc_dist = 0.1 * pd

    lu = (0.2, 0.8)
    ru = (0.2 + inc_dist, 0.8)
    ld = (0.2, 0.8 - inc_dist)
    rd = (0.2 + inc_dist, 0.8 - inc_dist)

    puddle_1 = np.array([lu, ru, ld, rd])

    rd = (0.8, 0.2)
    ld = (0.8 - inc_dist, 0.2)
    ru = (0.8, 0.2 + inc_dist)
    lu = (0.8 - inc_dist, 0.2 + inc_dist)

    puddle_2 = np.array([lu, ru, ld, rd])

    return puddle_1, puddle_2

#####################################################################
# get_goal()
# -------------------------------------------------------------------
#####################################################################
def get_goal():
    dim = 3
    dist = 0.1 * dim

    rd = (1, 1-dist)
    ld = (1-dist, 1-dist)
    ru = (1, 1)
    lu = (1-dist, 1)

    goal = np.array([lu, ru, ld, rd])

    return goal


#####################################################################
# get_best_action(data)
# -------------------------------------------------------------------
# Description: returns the best action given a set of data
# Returns: best action and whether or not the agent is in a puddle
#####################################################################
def get_best_action(data):
    x, y, f1, f2 = data
    puddle_1, puddle_2 = get_puddles(puddle_dim)

    if f1 and is_in_puddle(x, y, puddle_1):
        return 2

    if f2 and is_in_puddle(x, y, puddle_2):
        return 1

    return 0


#####################################################################
# generate_init_data(n_data)
# -------------------------------------------------------------------
#####################################################################
def generate_init_data(n_data):
    data = []
    for i in range(n_data):
        x, y = random.uniform(0, 1), random.uniform(0, 1)
        f1, f2 = randint(0, 1), randint(0, 1)
        a = get_best_action([x, y, f1, f2])

        data.append([x, y, f1, f2, a])

    return array(data)


#####################################################################
# get_human_reinf_from_prev_step(data):
# -------------------------------------------------------------------
# Description: Tries to model a human reinforcement policy
# Returns: (-1 if in puddle, 0 if not in puddle, 1 if in goal)
#####################################################################
def get_human_reinf_from_prev_step(data):
    if not data:
        return 0

    x, y, f1, f2, a = data

    # If agent is in a puddle
    if (f1 and is_in_puddle(x, y, puddle_1)) \
            or (f2 and is_in_puddle(x, y, puddle_2)):
        return -1

    else:
        return 0


def tamer_algorithm(stepSize):
    # while True:
    # h = getHumanReinfSincePreviousTimeStep(data)

    pass


generate_init_data(50)

if __name__ == '__main__':
    tamer_algorithm(stepSize=1)

# Up: 1, Right: 2, Down: 3, Left: 4
# xmpl_X = np.array([
#     [0.2, 0.8, 1, 0, 2],
#     [0.25, 0.75, 1, 0, 2],
#     [0.8, 0.8, 0, 0, 1],
#     [0.7, 0.7, 0, 0, 1],
#     [0.2, 0.2, 1, 0, 1],
#     [0.2, 0.8, 1, 0, 1]])
#
# xmpl_Y = np.array([-1, -1, 1, 1, 0, 0])
# reg = LinearRegression().fit(xmpl_X, xmpl_Y)
# test_X = np.array([[0.2, 0.8, 0, 1, 2]])
#
# data = [0.25, 0.75, 1, 0]
# print(get_best_action(data))
