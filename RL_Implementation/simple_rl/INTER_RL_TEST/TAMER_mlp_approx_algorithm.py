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

epsilon = 0.75

explanatory_actions = ["No Explanation", "Puddle #1 is shallow", "Puddle #2 is shallow", "All puddles are shallow"]


def get_best_action(state, actions_models, acts, explanation_features):
    # In this function we have to select the best action to take
    xf = explanation_features
    best_act = 0
    best_h = -np.inf

    for i, act in enumerate(acts):
        X_to_predict = np.array([[state.x, state.y, i, xf[0], xf[1], xf[2]]])

        model_name = 'nn_model_{}'.format(act)
        aux = actions_models[model_name].predict(X_to_predict).flatten()[0]
        if aux > best_h:
            best_h = aux
            best_act = i

    print ("best action",i,best_h)
    return best_act

def epsilon_greedy(state, actions_models, acts, explanation_features):
    # Policy: Epsilon of the time explore, otherwise, greedyQ.
    global epsilon
    if np.random.random() > epsilon:
        # Exploit.
        action_id = get_best_action(state, actions_models, acts, explanation_features)
    else:
        # Explore
        action_id = np.random.randint(0, len(acts))

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

    model.add(Dense(10, input_shape=(6,)))
    model.add(Dense(1))
    model.compile(optimizer='sgd', loss=['mean_absolute_error'], metrics=['accuracy'])

    return model

def get_action_models_and_training_sets(actions):
    actions_models = {}
    actions_X_train = {}
    actions_y_train = {}
    aux_X_train = {}
    aux_y_train = {}
    for a in actions:
        actions_models['nn_model_{}'.format(a)] = make_model()
        actions_X_train['X_train_{}'.format(a)] = []
        actions_y_train['y_train_{}'.format(a)] = []
        aux_X_train['X_train_{}'.format(a)] = []
        aux_y_train['y_train_{}'.format(a)] = []

    return actions_models, actions_X_train, actions_y_train, aux_X_train, aux_y_train


def load_trained_actions_models(actions):
    weights_file_str = 'weights/weights_{}.hdf5'
    actions_models = {}

    # Init each model
    for a in actions:
        model_name = 'nn_model_{}'.format(a)
        weights_file = weights_file_str.format(a)

        actions_models[model_name] = make_model()
        actions_models[model_name].load_weights(weights_file)

    return actions_models

#####################################################################
# tamer_algorithm(stepSize)
# -------------------------------------------------------------------
# Description: Implementation of the TAMER algorithm
#####################################################################
def tamer_algorithm():
    weights_file_str = 'weights/weights_{}.hdf5'

    puddy = PUDDLER()
    init_state = puddy.get_initial_state()
    all_actions = puddy.get_possible_actions()
    current_act_ind = randint(0, len(all_actions) - 1)

    EPISODE_LIMIT = 40
    episode_count = 0

    actions_models, actions_X_train, actions_y_train, aux_X_train, aux_y_train \
        = get_action_models_and_training_sets(all_actions)

    current_state = puddy.get_next_state(init_state, all_actions[current_act_ind])
    # current_act_ind = epsilon_greedy(current_state, actions_models, all_actions, explanation_features)

    start_time = time.time()

    batch_size = 250
    num_iters = 10*500
    for i in range(num_iters):
        prev_best_action = all_actions[current_act_ind]
        model_name = 'nn_model_{}'.format(prev_best_action)
        X_train_name = 'X_train_{}'.format(prev_best_action)
        y_train_name = 'y_train_{}'.format(prev_best_action)

        explanation_features = choose_random_expln_features()
        episode_count += 1
        # Get the human reward:
        h = puddy.get_human_reinf_from_prev_step(current_state, all_actions[current_act_ind], explanation_features)
        aux_y_train[y_train_name].append(h)

        print ("prev_best_action",current_state,prev_best_action,h)
        xf = explanation_features
        aux_X_train[X_train_name].append([current_state.x, current_state.y, current_act_ind, xf[0], xf[1], xf[2]])
        actions_X_train[X_train_name] = np.array(aux_X_train[X_train_name])
        actions_y_train[y_train_name] = np.array(aux_y_train[y_train_name])

        # If have a batch of data ready, train and predict from it
        # Update the models if we are on a batch_size iteration
        if i % batch_size == 0:
            for poss_act in all_actions:
                train_weights_file = weights_file_str.format(poss_act)
                train_model_name = 'nn_model_{}'.format(poss_act)
                train_X_name = 'X_train_{}'.format(poss_act)
                train_y_name = 'y_train_{}'.format(poss_act)

                curr_model = actions_models[train_model_name]

                try:
                    curr_model.load_weights(train_weights_file)
                except:
                    pass
                print("----------------------------------")
                print "IN ITERATION {}".format(i)
                print("TRAINING {}".format(prev_best_action))
                X_train = actions_X_train[train_X_name]
                y_train = actions_y_train[train_y_name]
                if len(X_train) > 0:
                    curr_model.fit(X_train, y_train, nb_epoch=20, batch_size=2)
                    curr_model.save_weights(train_weights_file)
                else:
                    print ("actions ",poss_act)

        # Get the next state based on action (random for the moment)
        new_state = puddy.get_next_state(current_state, all_actions[current_act_ind])

        # This is the predict part
        current_act_ind = epsilon_greedy(new_state, actions_models, all_actions, explanation_features)
        # print ("current action", all_actions[current_act_ind])
        current_state = copy.deepcopy(new_state)

        if current_state.is_terminal() or episode_count >= EPISODE_LIMIT:
            current_state = puddy.get_initial_state()
            episode_count = 0

    elapsed_time = time.time() - start_time
    print ("------------------------------------------------------------")
    print (" Elapsed time to train: {}".format(elapsed_time))
    print ("------------------------------------------------------------")

    # ------------ EVAL --------------  #
    actions_models = load_trained_actions_models(all_actions)
    # -------------------------------- #

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

    current_state = puddy.get_initial_state()
    print("Best action from tamer",
          all_actions[get_best_action(current_state, actions_models, all_actions, explanation_features)])

    puddy.visualize_agent(current_state)
    curr_char = raw_input("")
    while curr_char.lower() != 'n':
        a = all_actions[get_best_action(current_state, actions_models, all_actions, explanation_features)]
        print("Next action", a)
        next_state = puddy.get_next_state(current_state, a)
        print("New state", next_state)
        current_state = copy.deepcopy(next_state)
        puddy.visualize_agent(current_state)
        curr_char = raw_input("")


if __name__ == '__main__':
    tamer_algorithm()
