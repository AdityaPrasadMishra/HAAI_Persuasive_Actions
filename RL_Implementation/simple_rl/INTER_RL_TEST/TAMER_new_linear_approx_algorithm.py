import time
import copy
import random
import numpy as np
from numpy import array
from random import randint
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from Human_Interface import PUDDLER
from LinearTamerApprox import LinearFuncApprox
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

epsilon=0.5

explanatory_actions = ["No Explanation", "Puddle #1 is shallow", "Puddle #2 is shallow", "All puddles are shallow"]

def get_best_action(state, model, acts, explanation_features):
    curr_best_act_index = 0
    #np_s = np.array([list(state.features())+explanation_features+[curr_best_act_index]])
    curr_best_act_val = model.get_q_value(state, np.array(explanation_features), acts[curr_best_act_index])
    # Equality check
    equal_flag = True
    for curr_index in range(len(acts)):
        curr_val =  model.get_q_value(state, np.array(explanation_features), acts[curr_index])
        #print ("act",acts[curr_index], curr_val)
        if curr_val > curr_best_act_val:
            curr_best_act_val = curr_val
            curr_best_act_index = curr_index
        if curr_val != curr_best_act_val:
            equal_flag = False
    
    if equal_flag:
        print ("we reached here")
        curr_best_act_index = randint(0, len(acts)-1)
    return curr_best_act_index



def epsilon_greedy(state, model, acts, explanation_features):
    # Policy: Epsilon of the time explore, otherwise, greedyQ.
    global epsilon
    if np.random.random() > epsilon:
        # Exploit.
        action_id = get_best_action(state, model, acts, explanation_features)
    else:
        # Explore
        action_id = np.random.randint(0, len(acts)-1)

    return action_id



def choose_random_expln_features():
    global explanatory_actions
    exp = random.choice(explanatory_actions)

    if explanatory_actions.index(exp) == 0:
        return [0,0,0]
    elif explanatory_actions.index(exp) == 1:
        return [1,0,0]
    elif explanatory_actions.index(exp) == 2:
        return [0,1,0]
    elif explanatory_actions.index(exp) == 3:
        return [0,0,1]

#####################################################################
# tamer_algorithm(stepSize)
# -------------------------------------------------------------------
# Description: Implementation of the TAMER algorithm
#####################################################################
def tamer_algorithm():


    puddy = PUDDLER()

    init_state = puddy.get_initial_state()
    all_actions = puddy.get_possible_actions()
    
    explanation_features = [0,0,0]

    
    
    current_act_ind = randint(0,len(all_actions)-1)

    #X_train = np.array([list(init_state.features()) + explanation_features +[current_act_ind]])
    #y_train = np.array([puddy.get_human_reinf_from_prev_step(init_state, all_actions[current_act_ind], explanation_features)])

    # Fit the values from the data
    #reg = SGDRegressor(max_iter=100).fit(X_train, y_train)
    approx_model = LinearFuncApprox(num_features = 5,actions=all_actions)
    approx_model.update(init_state, np.array(explanation_features), all_actions[current_act_ind], puddy.get_human_reinf_from_prev_step(init_state, all_actions[current_act_ind], explanation_features))

    # s = [x, y, p1, p2, a]
    # Up: 1, Right: 2, Down: 3, Left: 4
    #s = [0.1, 0.1, 1, 0]
    #a = get_best_action(s)

    #s.append(a)
    #np_s = np.array([s])

    current_state = puddy.get_next_state(init_state, all_actions[current_act_ind])
    current_act_ind = epsilon_greedy(current_state, approx_model, all_actions, explanation_features)

    EPISODE_LIMIT = 100
    episode_count = 0

    # choose a random explanatory action
    for i in range(100000):
        explanation_features = choose_random_expln_features()
        episode_count += 1
        # Get the human reward:
        h = puddy.get_human_reinf_from_prev_step(current_state, all_actions[current_act_ind], explanation_features)
        # We assume that the human model is optimal
        #if h != 0:
            # Online learning:
#        print(current_state, h, all_actions[current_act_ind])
        approx_model.update(current_state, np.array(explanation_features), all_actions[current_act_ind], h)

        # Get the next state based on action (random for the moment)
        new_state = puddy.get_next_state(current_state, all_actions[current_act_ind])
        current_act_ind = epsilon_greedy(new_state, approx_model, all_actions, explanation_features)
        #print ("current action", all_actions[current_act_ind])
        current_state = copy.deepcopy(new_state)

        if current_state.is_terminal() or episode_count >= EPISODE_LIMIT:
            current_state = puddy.get_initial_state()
            episode_count = 0

    
    explanation_features = [0,0,0]
    # Test the policy
    current_state = puddy.get_initial_state()
    print ("Start from state",current_state)
    print ("Best action from tamer",all_actions[get_best_action(current_state, approx_model, all_actions, explanation_features)])
    curr_char = "S"
    puddy.visualize_agent(current_state)
    curr_char = raw_input("")
    while curr_char.lower() != 'n':

        a = puddy.get_best_action(current_state)
        print ("Next action", a)
        next_state = puddy.get_next_state(current_state, a)
        print ("New state", next_state)
        current_state = copy.deepcopy(next_state)
        puddy.visualize_agent(current_state)
        curr_char = raw_input("")
        #ime.sleep(1)




if __name__ == '__main__':
    tamer_algorithm()

