import time
import copy
import random
import numpy as np
from numpy import array
from random import randint
# from sklearn.linear_model import LinearRegression
# from sklearn.linear_model import SGDRegressor

from Human_Interface import PUDDLER
from keras.models import Sequential
from keras.layers import Dense
from LinearTamerApprox import LinearFuncApprox

#####################################################################
# Initialize reinforcement model with the stepSize                  #
# Vector of states s init to 0                                      #
# s = 0                                                             #
# Vector of features f init to 0                                    #
# f = 0                                                             #
# while true:                                                       #
# h = getHumanReinfbasedOnFeatures                                  #
# if h != 0:                                                        #
#      error = h - PredictionOfTheModelGivenFeatures(f)             #
#      UpdateReinfModel(f, error)                                   #
#   s = GetVectorOfStates                                           #
#   a = argmax(ReinfModel.predict(getFeatures(s, a)))               #
#   f = getFeatures(s, a)                                           #
#   takeAction(a)                                                   #
#   waitForNextTimestep                                             #
#####################################################################

epsilon = 0.5

explanatory_actions = ["No Explanation", "Puddle #1 is shallow", "Puddle #2 is shallow", "All puddles are shallow"]


def get_best_action(state, model, acts, explanation_features):
    curr_best_act_index = 0
    # np_s = np.array([list(state.features())+explanation_features+[curr_best_act_index]])
    curr_best_act_val = model.get_q_value(state, np.array(explanation_features), acts[curr_best_act_index])
    # Equality check
    equal_flag = True
    for curr_index in range(len(acts)):
        curr_val = model.get_q_value(state, np.array(explanation_features), acts[curr_index])
        # print ("act",acts[curr_index], curr_val)
        if curr_val > curr_best_act_val:
            curr_best_act_val = curr_val
            curr_best_act_index = curr_index
        if curr_val != curr_best_act_val:
            equal_flag = False

    if equal_flag:
        print("we reached here")
        curr_best_act_index = randint(0, len(acts) - 1)
    return curr_best_act_index


def epsilon_greedy(state, model, acts, explanation_features):
    # Policy: Epsilon of the time explore, otherwise, greedyQ.
    global epsilon
    if np.random.random() > epsilon:
        # Exploit.
        action_id = get_best_action(state, model, acts, explanation_features)
    else:
        # Explore
        action_id = np.random.randint(0, len(acts) - 1)

    return action_id


def choose_random_expln_features():
    global explanatory_actions
    exp = random.choice(explanatory_actions)

    if explanatory_actions.index(exp) == 0:
        return [0, 0, 0]
    elif explanatory_actions.index(exp) == 1:
        return [1, 0, 0]
    elif explanatory_actions.index(exp) == 2:
        return [0, 1, 0]
    elif explanatory_actions.index(exp) == 3:
        return [0, 0, 1]

def make_model():
    model = Sequential()

    model.add(Dense(2, input_shape=(6,)))
    model.add(Dense(2, activation='relu'))
    model.add(Dense(2, activation='relu'))
    model.add(Dense(1))

    return model


#####################################################################
# tamer_algorithm(stepSize)
# -------------------------------------------------------------------
# Description: Implementation of the TAMER algorithm
#####################################################################
def tamer_algorithm():
    puddy = PUDDLER()

    init_state = puddy.get_initial_state()
    all_actions = puddy.get_possible_actions()

    explanation_features = [0, 0, 0]

    current_act_ind = randint(0, len(all_actions) - 1)

    # Fit the values from the data
    # reg = SGDRegressor(max_iter=100).fit(X_train, y_train)
    approx_model = LinearFuncApprox(num_features=5, actions=all_actions)
    approx_model.update(init_state, np.array(explanation_features), all_actions[current_act_ind],
                        puddy.get_human_reinf_from_prev_step(init_state, all_actions[current_act_ind],
                                                             explanation_features))

    current_state = puddy.get_next_state(init_state, all_actions[current_act_ind])
    current_act_ind = epsilon_greedy(current_state, approx_model, all_actions, explanation_features)

    EPISODE_LIMIT = 100
    episode_count = 0

    # ------------------------- #
    X = []
    y = []
    nn_model = make_model()
    nn_model.compile(optimizer='sgd', loss=['mse'], metrics=['accuracy'])
    # ------------------------- #

    for i in range(100):

        explanation_features = choose_random_expln_features()
        episode_count += 1
        # Get the human reward:
        h = puddy.get_human_reinf_from_prev_step(current_state, all_actions[current_act_ind], explanation_features)

        xf = explanation_features
        X.append([current_state.x, current_state.y, current_act_ind, xf[0], xf[1], xf[2]])
        y.append(h)

        X_train = np.array(X)
        y_train = np.array(y)
        #TODO: The amount of epochs has to decrease as more data comes
        epochs = 400
        if X_train.shape[0] % 1000:
            epochs = 400 - (X_train.shape[0]/1000)*10

        nn_model.fit(X_train, y_train, nb_epoch=epochs)

        # We assume that the human model is optimal
        # if h != 0:
        # Online learning:
        #        print(current_state, h, all_actions[current_act_ind])
        approx_model.update(current_state, np.array(explanation_features), all_actions[current_act_ind], h)

        # Get the next state based on action (random for the moment)
        new_state = puddy.get_next_state(current_state, all_actions[current_act_ind])
        current_act_ind = epsilon_greedy(new_state, approx_model, all_actions, explanation_features)
        # print ("current action", all_actions[current_act_ind])
        current_state = copy.deepcopy(new_state)

        if current_state.is_terminal() or episode_count >= EPISODE_LIMIT:
            current_state = puddy.get_initial_state()
            episode_count = 0

    print "--------- MODEL EVAL ----------- "
    print nn_model.evaluate(X_train, y_train)
    print "-------------------------------- "

    explanation_features = [0, 0, 0]
    # Test the policy
    current_state = puddy.get_initial_state()
    print("Start from state", current_state)
    curr_char = "S"
    puddy.visualize_agent(current_state)
    curr_char = raw_input("")
    while curr_char.lower() != 'n':
        a = puddy.get_best_action(current_state)
        print("Next action", a)
        next_state = puddy.get_next_state(current_state, a)
        print("New state", next_state)
        current_state = copy.deepcopy(next_state)
        puddy.visualize_agent(current_state)
        curr_char = raw_input("")
        # ime.sleep(1)

    current_state = puddy.get_initial_state()
    print("Best action from tamer",
          all_actions[get_best_action(current_state, approx_model, all_actions, explanation_features)])

    puddy.visualize_agent(current_state)
    curr_char = raw_input("")
    while curr_char.lower() != 'n':
        a = all_actions[get_best_action(current_state, approx_model, all_actions, explanation_features)]
        print("Next action", a)
        next_state = puddy.get_next_state(current_state, a)
        print("New state", next_state)
        current_state = copy.deepcopy(next_state)
        puddy.visualize_agent(current_state)
        curr_char = raw_input("")


if __name__ == '__main__':
    tamer_algorithm()
