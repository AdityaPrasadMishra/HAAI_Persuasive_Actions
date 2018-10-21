from collections import defaultdict
import sys

# Use local files
import srl_example_setup


from simple_rl.agents import QLearningAgent, RandomAgent
from simple_rl.agents.func_approx.LinearQAgentClass import LinearQAgent
from simple_rl.tasks import GridWorldMDP, GridWorldState
from simple_rl.run_experiments import run_single_agent_on_mdp
# Two Puddles
from simple_rl.tasks.puddle.PuddleMDPClass import PuddleMDP
# Only Puddles #1
from simple_rl.tasks.puddle.PuddleMDPClass2 import PuddleMDP2
# Only Puddles #2
from simple_rl.tasks.puddle.PuddleMDPClass3 import PuddleMDP3
# No puddles
from simple_rl.tasks.puddle.PuddleMDPClass4 import PuddleMDP4





class PUDDLER:
    def __init__(self):
        self.base_human_model = PuddleMDP()
        self.base_agent = LinearQAgent(actions=self.base_human_model.get_actions(),num_features=2, epsilon=0.5)
        run_single_agent_on_mdp(self.base_agent, self.base_human_model, episodes=1000, steps=100, verbose=True)
        self.test_run = True

        if self.test_run:
            self.novice_model_1 = self.base_human_model
            self.novice_model_2 = self.base_human_model
            self.fully_actulized_model = self.base_human_model

            self.novice_agent_1 = self.base_agent
            self.novice_agent_2 = self.base_agent
            self.fully_actulized_agent = self.base_agent
        else:
            self.novice_model_1 = PuddleMDP2()
            self.novice_agent_1 = LinearQAgent(actions=self.novice_model_1.get_actions(),num_features=2)
            run_single_agent_on_mdp(self.novice_agent_1, self.novice_model_1, episodes=10000, steps=4)

            self.novice_model_2 = PuddleMDP3()
            self.novice_agent_2 = LinearQAgent(actions=self.novice_model_2.get_actions(),num_features=2)
            run_single_agent_on_mdp(self.novice_agent_2, self.novice_model_2, episodes=10000, steps=4)

            self.fully_actulized_model = PuddleMDP4()
            self.fully_actulized_agent = LinearQAgent(actions=self.fully_actulized_model.get_actions(),num_features=2)
            run_single_agent_on_mdp(self.fully_actulized_agent, self.fully_actulized_model, episodes=10000, steps=4)


        # TODO Add other settings

        self.current_agent = self.base_agent
        self.current_mdp = self.base_human_model

    def get_init_info(self):
        data_points = []
        return data_points

    def get_human_reinf_from_prev_step(self, state, action, explanation_features=[0,0,0]):
        if explanation_features[2] == 1 or (explanation_features[1] == 1 and explanation_features[0] == 1):
            self.current_mdp = self.fully_actulized_model
            self.current_agent = self.fully_actulized_agent
        elif explanation_features[0] == 1:
            self.current_mdp = self.novice_model_1
            self.current_agent = self.novice_agent_1
        elif explanation_features[1] == 1:
            self.current_mdp = self.novice_model_2
            self.current_agent = self.novice_agent_2
        else:
            self.current_mdp = self.base_human_model
            self.current_agent = self.base_agent

        curr_best_q_val = self.current_agent.get_value(state)
        curr_q_val = self.current_agent.get_q_value(state, action) 
        return curr_q_val - curr_best_q_val


    def get_possible_actions(self):
        return self.base_human_model.get_actions()

    def get_best_action(self,state):
        return self.base_agent.get_max_q_action(state)


    def get_initial_state(self):
        # TODO Randomize
        return self.base_human_model.get_init_state()

    def get_initial_state_features(self):
        return self.base_human_model.get_init_state().features()

    def get_next_state(self,state,act):
        self.base_human_model.set_state(state)
        reward, new_state = self.base_human_model.execute_agent_action(act)
        return new_state

    #def is_current_state_terminal(self,state):

    def visualize_agent(self, state):
        self.base_human_model.set_state(state)
        self.base_human_model.visualize_state(self.base_agent)


if __name__ == "__main__":
    test_puddy = PUDDLER()
    a = test_puddy.get_initial_state()
    test_puddy.current_mdp.visualize_agent(test_puddy.current_agent)
