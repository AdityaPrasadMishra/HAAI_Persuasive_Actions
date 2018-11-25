import pddlpy
import sys
import copy
from plan_executor import Executor
from Search import *


ALPHA = 1.0

class Problem:

    def __init__(self, robot_domain_model, robot_problem, plan_file, explanatory_actions_file, max_expl_length):

        self.exc_obj = Executor(robot_domain_model, robot_problem, plan_file)
        #self.exc_obj = copy.deepcopy(exc.get_beh_trace())
        self.max_expl_length = max_expl_length
        
        with open(explanatory_actions_file) as e_fd:
            self.action_set = set([a.strip() for a in e_fd.readlines()])


    def explain(self):
        start_state = SearchNode(set(), self.action_set, [], self.exc_obj, ALPHA)

        final_explanation = Exhaustive_Search(start_state)

        return final_explanation



