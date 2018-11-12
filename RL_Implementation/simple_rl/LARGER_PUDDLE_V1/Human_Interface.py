from collections import defaultdict
import sys

# Use local files
import srl_example_setup


from simple_rl.agents import QLearningAgent, RandomAgent
from simple_rl.agents.ModQLearningAgentClass import ModQLearningAgent
from simple_rl.agents.func_approx.LinearQAgentClass import LinearQAgent
from simple_rl.agents.func_approx.GradientBoostingAgentClass import GradientBoostingAgent
from simple_rl.tasks import GridWorldMDP, GridWorldState
from simple_rl.run_experiments import run_single_agent_on_mdp
# Two Puddles
from simple_rl.tasks.puddle.PuddleMDPClass import PuddleMDP
# No puddles
from simple_rl.tasks.puddle.PuddleMDPClass2 import PuddleMDP2
# No puddles
from simple_rl.tasks.puddle.PuddleMDPClass3 import PuddleMDP3
# No puddles
from simple_rl.tasks.puddle.PuddleMDPClass4 import PuddleMDP4

from simple_rl.planning.ValueIterationClass import ValueIteration 




class PUDDLER:
    def __init__(self):
        self.base_human_model = PuddleMDP(step_cost=1.0)
        self.base_agent = ValueIteration(self.base_human_model,max_iterations=5000,sample_rate=1)
        self.sample_agent = ModQLearningAgent(actions=self.base_human_model.get_actions(), epsilon=0.5, anneal=True)
        #run_single_agent_on_mdp(self.base_agent, self.base_human_model, episodes=10000, steps=60, verbose=True)
        self.base_agent.run_vi()

        #print ("Q func", self.base_agent.q_func)
        self.test_run = False

        if self.test_run:
            self.novice_model_1 = self.base_human_model
            self.novice_model_2 = self.base_human_model
            self.fully_actulized_model = self.base_human_model

            self.novice_agent_1 = self.base_agent
            self.novice_agent_2 = self.base_agent
            self.fully_actulized_agent = self.base_agent
        else:

            self.novice_model_1 = PuddleMDP2(step_cost=1.0)
            self.novice_agent_1 = ValueIteration(self.novice_model_1)
            self.novice_agent_1.run_vi()
            

            self.novice_model_2 = PuddleMDP3(step_cost=1.0)
            self.novice_agent_2 = ValueIteration(self.novice_model_2)
            self.novice_agent_2.run_vi()


            self.fully_actulized_model = PuddleMDP4(step_cost=1.0)
            self.fully_actulized_agent = ValueIteration(self.fully_actulized_model)
            self.fully_actulized_agent.run_vi()
            #self.fully_actulized_agent = ModQLearningAgent(actions=self.fully_actulized_model.get_actions(), epsilon=0.5, anneal=True)
            #run_single_agent_on_mdp(self.fully_actulized_agent, self.fully_actulized_model, episodes=10000, steps=60, verbose=True)


        # TODO Add other settings

        self.current_agent = self.base_agent
        self.current_mdp = self.base_human_model

    def get_init_info(self):
        data_points = []
        return data_points

    def get_human_reinf_from_prev_step(self, state, action, explanation_features=[0,0]):
        delta = 0.1
        print (explanation_features)
        if explanation_features[1] == 1 and explanation_features[0] == 1:
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
#        return curr_q_val - curr_best_q_val
        return min((float(curr_best_q_val - curr_q_val)+delta)/(float(curr_best_q_val)+delta),1)


    def get_possible_actions(self):
        return self.base_human_model.get_actions()

    def get_best_action(self,state, explanation_features=[0,0]):
        if explanation_features[1] == 1 and explanation_features[0] == 1:
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
        
        return self.current_agent._get_max_q_action(state)


    def get_initial_state(self):
        # TODO Randomize
        return self.base_human_model.get_init_state()

    def get_initial_state_features(self):
        return self.base_human_model.get_init_state().features()

    def get_next_state(self,state,act, explanation_features=[0]):
        if explanation_features[0] >= 0.5:
            self.current_mdp = self.fully_actulized_model
            self.current_agent = self.fully_actulized_agent
        else:
            self.current_mdp = self.base_human_model
            self.current_agent = self.base_agent

        self.current_mdp.set_state(state)
        reward, new_state = self.current_mdp.execute_agent_action(act)
        return new_state

    def set_state(self,x,y):
        state = GridWorldState(x,y)
        self.base_human_model.set_state(state)
        return state

    def visualize_agent(self, state):
        self.base_human_model.set_state(state)
        self.base_human_model.visualize_state(self.sample_agent)


if __name__ == "__main__":
    test_puddy = PUDDLER()
    a = test_puddy.get_initial_state()
    state = test_puddy.current_mdp.get_init_state()
    test_puddy.current_agent.get_max_q_value(state)

    for k in test_puddy.current_agent.q_func:
        print (k,test_puddy.current_agent.q_func[k])
    test_puddy.current_mdp.visualize_agent(test_puddy.current_agent)
