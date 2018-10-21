'''
LinearQLearningAgentClass.py

Contains implementation for a Q Learner with a Linear Function Approximator.
'''

# Python imports.
import numpy as np
import math
from collections import defaultdict

# Other imports.
#from simple_rl.agents import Agent, QLearningAgent

class LinearFuncApprox:
    '''
    QLearningAgent with a linear function approximator for the Q Function.
    '''

    def __init__(self, num_features,actions, rand_init=True, alpha=0.2, rbf=False, anneal=True):
        self.actions = actions
        name = "Approx-T" #+ "-rbf" if rbf else name
        self.num_features = num_features
        self.rand_init = rand_init
        self.alpha = alpha
        # Add a basis feature.
        if rand_init:
            self.weights = np.random.random(self.num_features*len(self.actions))
        else:
            self.weights = np.zeros(self.num_features*len(self.actions))

        self.rbf = rbf

    def get_parameters(self):
        '''
        Returns:
            (dict) key=param_name (str) --> val=param_val (object).
        '''
        param_dict = defaultdict(int)
        
        param_dict["num_features"] = self.num_features
        param_dict["rand_init"] = self.rand_init
        param_dict["alpha"] = self.alpha
        param_dict["rbf"] = self.rbf
        param_dict["anneal"] = self.anneal
        param_dict["explore"] = self.explore

        return param_dict

    def update(self, state, action, val):
        '''
        Args:
            state (State)
            action (str)
            reward (float)
            next_state (State)

        Summary:
            Updates the internal Q Function according to the Bellman Equation. (Classic Q Learning update)
        '''
        self._update_weights(state, action, val)

    def _phi(self, state, action):
        '''
        Args:
            state (State): The abstract state object.
            action (str): A string representing an action.

        Returns:
            (numpy array): A state-action feature vector representing the current State and action.

        Notes:
            The resulting feature vector multiplies the state vector by |A| (size of action space), and only the action passed in retains
            the original vector, all other values are set to 0.
        '''
        result = np.zeros(self.num_features * len(self.actions))
        act_index = self.actions.index(action)

        basis_feats = state.features()

        if self.rbf:
            basis_feats = [_rbf(f) for f in basis_feats]

        result[act_index*self.num_features:(act_index + 1)*self.num_features] = basis_feats

        return result

    def _update_weights(self, cur_state, action, val):
        '''
        Args:
            reward (float)
            cur_state (State)

        Summary:
            Updates according to:

            [Eq. 1] delta = r + gamma * max_b(Q(s_curr,b)) - Q(s_prev, a_prev)

            For each weight:
                w_i = w_i + alpha * phi(s,a)[i] * delta

            Where phi(s,a) maps the state action pair to a feature vector (see QLearningAgent._phi(s,a))
        '''

        # Compute temporal difference [Eq. 1]
        max_q_cur_state = self.get_q_value(cur_state, action)
        #prev_q_val = self.get_q_value(self.prev_state, self.prev_action)
        self.most_recent_loss = val - max_q_cur_state 

        # Update each weight
        phi = self._phi(cur_state, action)
        active_feats_index = self.actions.index(action) * self.num_features

        # Sparsely update the weights (only update weights associated with the action we used).
        for i in range(active_feats_index, active_feats_index + self.num_features):
            self.weights[i] = self.weights[i] + self.alpha * phi[i] * self.most_recent_loss

    def get_q_value(self, state, action):
        '''
        Args:
            state (State): A State object containing the abstract state representation
            action (str): A string representing an action. See namespaceAIX.

        Returns:
            (float): denoting the q value of the (@state,@action) pair.
        '''

        # Return linear approximation of Q value
        sa_feats = self._phi(state, action)

        return np.dot(self.weights, sa_feats)

    def reset(self):
        self.weights = np.zeros(self.num_features*len(self.actions))
        QLearningAgent.reset(self)


def _rbf(x):
    return math.exp(-(x)**2)
