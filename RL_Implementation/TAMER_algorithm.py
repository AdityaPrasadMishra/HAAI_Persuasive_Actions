import random
import numpy as np
from numpy import array
from random import randint
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor


# TODO: Do this via online learning

#####################################################################
# Initialize reinforcement model with the stepSize                  #
# Vector of states s init to 0                                      #
# s = 0                                                             #
# Vector of features f init to 0                                    #
# f = 0                                                             #
# while true:                                                       #
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

puddle_dim = 5
goal_dim = 2

#####################################################################
# is_in_location(min_x, max_x, min_y, max_y)
# -------------------------------------------------------------------
#####################################################################
def is_in_location(x, y, location):
    min_x = location[0][0]
    max_x = location[3][0]
    min_y = location[3][1]
    max_y = location[0][1]

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
    dist = 0.1 * goal_dim

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
    data = list(data)

    x, y, f1, f2 = data
    puddle_1, puddle_2 = get_puddles(puddle_dim)

    if f1 and is_in_location(x, y, puddle_1):
        return 2

    if f2 and is_in_location(x, y, puddle_2):
        return 1

    return randint(1, 4)


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
# get_human_reinf_from_prev_step(data)
# -------------------------------------------------------------------
# Description: Tries to model a human reinforcement policy
# Returns: (-1 if in puddle, 0 if not in puddle, 1 if in goal)
#####################################################################
def get_human_reinf_from_prev_step(data):
    data = list(data)

    puddle_1, puddle_2 = get_puddles(puddle_dim)
    goal = get_goal()

    x, y, f1, f2, a = data

    # If agent is in a puddle
    if (f1 and is_in_location(x, y, puddle_1)) \
            or (f2 and is_in_location(x, y, puddle_2)):
        return -1

    # If agent is in the goal
    elif (is_in_location(x, y, goal)):
        return 1

    else:
        return 0

#####################################################################
# tamer_algorithm(stepSize)
# -------------------------------------------------------------------
# Description: Implementation of the TAMER algorithm
#####################################################################
def tamer_algorithm():

    random.seed(0)

    X_train = generate_init_data(50)
    y_train = np.array([get_human_reinf_from_prev_step(row) for row in X_train])

    # Fit the values from the data
    reg = SGDRegressor(max_iter=1000).fit(X_train, y_train)

    # s = [x, y, p1, p2, a]
    # Up: 1, Right: 2, Down: 3, Left: 4
    s = [0.1, 0.1, 1, 0]
    a = get_best_action(s)

    s.append(a)
    np_s = np.array([s])

    for i in range(100):

        # Get the human reward:
        h = get_human_reinf_from_prev_step(s)

        # We assume that the human model is optimal
        if h != 0:
            # Online learning:
            print(reg.predict(np_s))
            reg.partial_fit(np_s, np.array([h]))

        # Get the next state based on action (random for the moment)
        np_s = generate_init_data(1)
        s = list(np_s[0])


if __name__ == '__main__':
    tamer_algorithm()

