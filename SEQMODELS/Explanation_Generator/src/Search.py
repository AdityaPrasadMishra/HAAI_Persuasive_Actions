#!/usr/bin/env python

from queue import PriorityQueue, Queue
import copy
import os
import re
import subprocess
from plan_executor import Executor
from keras.models import Sequential, load_model,model_from_yaml
from keras.layers import Dense, Activation, CuDNNLSTM
from keras.optimizers import RMSprop, SGD
import random
import sys
import numpy as np
import time
'''
Method :: Astar Search
'''
GLOB_1 = 0

class SearchNode:
    def __init__(self, state = set(), action_set = set(), prefix = [], exc_obj = None, alpha = 1.0):
        self.current_state = state
        self.action_set = action_set
        self.prefix = prefix
        self.exc_obj = exc_obj 
        self.alpha = alpha

    def get_successors(self):
        poss_actions = self.action_set - self.current_state
        successor_list = []

        for act in poss_actions:
            new_state= self.current_state | set([act])
            new_node = SearchNode(new_state, self.action_set, self.prefix+[act], self.trace, self.alpha)
            successor_list.append(new_node)

        return successor_list

    #def get_next_state(self, act):


    def explanatory_action_feats(self):
        return " ".join(self.prefix)


    def get_new_trace(self, act):
        new_trace = []
        if act == "":
            exp_act_feats = ["",""]
        else:
            exp_act_feats = act.split(" ") #self.exc_obj.
        print ("feats",exp_act_feats)
        trace = self.exc_obj.execute_plan(exp_act_feats[0], exp_act_feats[1])
        #for i in range(len(trace)):
        #    new_trace.append(self.trace[i]+ " " + exp_act_feats)
        return trace

    def get_node_val(self, act):
        score = self.get_explicability_score(act)
        print (score)
        return self.alpha * self.get_explicability_score(act)

    def get_explicability_score(self, act):
        #try:
        maxval = 15
        START = 1000000000000000000000000000000000000000
        STOP  = 1100000000000000000000000000000000000000
        BLANK = 1110000000000000000000000000000000000000
        print ("In Explicabilty Score")
        new_trace = self.get_new_trace(act)
        print(new_trace)
        actual_trace = []
        actual_trace.append(START)
        for line in range(maxval):
                if line < len(new_trace):
                    actual_trace.append([[0]] +[list(map(int, x)) for x in new_trace[line]])
                else:
                    actual_trace.append(BLANK)
        actual_trace.append(STOP)        
        print(actual_trace)
        print("trace_printed")


        return 1.0 

       # except Exception as e:
        #    if hasattr(e, 'message'):
         #       print(e.message)
          #  else:
           #     print(e)
            #return "An Error Occured."

        # TODO: Mishraji will fill this in 



def Exhaustive_Search(start_state):

    fringe = Queue()
    closed = set()
    numberOfNodesExpanded = 0
    conflict_list = []
    current_sol = []

    fringe.put((0, start_state))

    node = start_state

    best_node_val = start_state.get_node_val("")
    best_expl = ""
    print ("Starting Search..")
#    while not fringe.empty():
    for act in start_state.action_set:
        print ("act",act)
        #node = fringe.get()[1]
        node_val = node.get_node_val(act)
        print ("node val found")
        if node_val > best_node_val:
            best_expl = act
            best_node_val = node_val

    return best_expl
