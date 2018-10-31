#!/usr/bin/env python

from queue import PriorityQueue, Queue
import copy
import os
import re
import subprocess
'''
Method :: Astar Search
'''


class SearchNode:
    def __init__(self, state = set(), action_set = set(), prefix = [], trace = [], alpha = 1.0):
        self.current_state = state
        self.action_set = action_set
        self.prefix = prefix
        self.trace = trace
        self.alpha = alpha

    def get_successors(self):
        poss_actions = action_set - self.current_state
        successor_list = []

        for act in poss_actions:
            new_state= self.current_state | set([act])
            new_node = SearchNode(new_state, self.action_set, self.prefix+[act], self.trace, self.alpha)
            successor_list.append(successor_list)

        return successor_list

    def explanatory_action_feats(self):
        return " ".join(self.prefix)


    def get_new_trace(self):
        new_trace = []
        exp_act_feats = self.explanatory_action_feats()
        for i in range(len(self.trace)):
            new_trace.append(self.trace[i]+ " " + exp_act_feats)
        return new_trace

    def get_node_val(self):
        return len(self.action_set) - len(self.trace) + self.alpha * self.get_explicability_score()

    def get_explicability_score(self):
        try:
            new_trace = str(self.get_new_trace())
            with open("feature_set_0_test", 'w') as out:
                for nt in new_trace:
                    out.write(nt + '\n')
            HAAISearchLocation = "/home/local/ASUAD/amishr28/HAAI_Persuasive_Actions/CRF_Implementation/Explanation_Generator/src"
            cmd ="cd "+ HAAISearchLocation+" &&"
            cmd += "java  -jar 'CRFModel.jar' &&" 
            cmd += " --model-file HAAICRFEXP feature_set_0_test &&" 
            cmd += "| grep 'Explicability Score :'"        
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            print('[DEBUG] Running command: {}'.format(cmd))
            print('[DEBUG] Output of Explicability Test: {}'.format(out))
            print('[DEBUG] Output of Explicability Test Error: {}'.format(err))
            outarr =out.split("Explicability Score :")[1]
            print(outarr)        
            out = float(outarr.strip())
            return out 

        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            return "An Error Occured."

        # TODO: Mishraji will fill this in 



def Exhaustive_Search(start_state, max_length = 2):

    fringe = Queue()
    closed = set()
    numberOfNodesExpanded = 0
    conflict_list = []
    current_sol = []

    fringe.put((0, start_state))

    best_node = start_state

    best_node_val = start_state.get_node_val()

    print ("Starting Search..")
    while not fringe.empty():
        node = fringe.get()[1]
        node_val = node.get_node_val()

        if node_val > best_node_val:
            best_node = node
            best_node_val = node_val

        if frozenset(node.current_state) not in closed and len(node.trace) <= max_length - 1:
            closed.add(frozenset(node[0]))

            successor_list         = problem.getSuccessors(node, old_plan)
            numberOfNodesExpanded += 1
            #print successor_list, node[1]
            if not numberOfNodesExpanded % 100:
                print ("Number of Nodes Expanded =", numberOfNodesExpanded)

            while successor_list:

                candidate_node = successor_list.pop()
                fringe.put((len(candidate_node.prefix), candidate_node))
    #print "curr", current_sol
    return best_node
