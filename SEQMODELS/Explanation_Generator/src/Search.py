#!/usr/bin/env python

from queue import PriorityQueue, Queue
import copy
import os
import re
import subprocess
from plan_executor import Executor

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
        global GLOB_1
        try:
            print ("We are Here")
            new_trace = self.get_new_trace(act)
            #with open("feature_set_"+str(GLOB_1)+"_test", 'w') as out:
            with open("feature_set_test", 'w') as out:
                for nt in new_trace:
                    out.write(nt + '\n')
            HAAISearchLocation = "/home/local/ASUAD/amishr28/HAAI_Persuasive_Actions/CRF_Implementation/Explanation_Generator/src"
            cmd =""
            #cmd += 'java "/home/local/ASUAD/ssreedh3/exp_wsp/mallet-2.0.8RC2/class/:/home/local/ASUAD/ssreedh3/exp_wsp/mallet-2.0.8RC2/lib/mallet-deps.jar" cc.mallet.fst.SimpleTagger --model-file nouncrf feature_set_test |grep "Exp :"|wc -l'
            cmd = 'java -cp  "/home/local/ASUAD/ssreedh3/exp_wsp/mallet-2.0.8RC2/class/:/home/local/ASUAD/ssreedh3/exp_wsp/mallet-2.0.8RC2/lib/mallet-deps.jar" cc.mallet.fst.SimpleTagger --model-file nouncrf feature_set_test |grep "UNEXP"|wc -l'
            print ("cmd:",cmd)
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            #outarr =str(out)#.split("Explicability Score :")[1].split("\\n")[0]
            #print("EXP score :"+ str(outarr))        
            #out = float(outarr.strip())
            #GLOB_1+=1
            return -1 * int(out) 

        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            return "An Error Occured."

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
