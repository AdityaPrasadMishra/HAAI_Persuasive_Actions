from random import randint
import numpy as np
from sklearn.linear_model import LinearRegression

# TODO: Do this via online learning

# Initialize reinforcement model with the stepSize
# Vector of states s init to 0
# s = 0
# Vector of features f init to 0
# f = 0
# while true:
# h = randint(-1, 1) # TODO: Change it to come from a function
# h = getHumanReinfbasedOnFeatures -> random for the moment
# if h != 0:
#      error = h - PredictionOfTheModelGivenFeatures(f)
#      UpdateReinfModel(f, error)
#   s = GetVectorOfStates
#   a = argmax(ReinfModel.predict(getFeatures(s, a)))
#   f = getFeatures(s, a)
#   takeAction(a)
#   waitForNextTimestep

puddle_dim = 1

# TODO: This can be shortened
def create_puddles(puddle_dim):
    inc_dist = 0.1 * puddle_dim

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

# TODO: This can be shortened
def get_best_action(data):
    x, y, f1, f2 = data
    puddle_1, puddle_2 = create_puddles(puddle_dim)

    if f1:
        min_x = puddle_1[0][0]
        max_x = puddle_1[3][0]
        min_y = puddle_1[3][1]
        max_y = puddle_1[0][1]

        print(min_x, max_x, min_y, max_y)

        if x >= min_x and x <= max_x:
            if y >= min_y and y <= max_y:
                return 2

    if f2:
        min_x = puddle_2[0][0]
        max_x = puddle_2[3][0]
        min_y = puddle_2[3][1]
        max_y = puddle_2[0][1]

        if x >= min_x and x <= max_x:
            if y >= min_y and y <= max_y:
                return 1

    return 0  # randint(1,4)


def tamer_algorithm(stepSize):
    pass


# Up: 1, Right: 2, Down: 3, Left: 4
xmpl_X = np.array([
    [0.2, 0.8, 1, 0, 2],
    [0.25, 0.75, 1, 0, 2],
    [0.8, 0.8, 0, 0, 1],
    [0.7, 0.7, 0, 0, 1],
    [0.2, 0.2, 1, 0, 1],
    [0.2, 0.8, 1, 0, 1]])

xmpl_Y = np.array([-1, -1, 1, 1, 0, 0])
reg = LinearRegression().fit(xmpl_X, xmpl_Y)
test_X = np.array([[0.2, 0.8, 0, 1, 2]])

data = [0.25, 0.75, 1, 0]
print(get_best_action(data))
