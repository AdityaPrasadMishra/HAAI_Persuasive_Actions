import pddlpy
import sys
import copy

class Executor:

    def __init__(self, robot_domain_model, robot_problem, plan_file):
        robot_dom_prob = pddlpy.DomainProblem(robot_domain_model, robot_problem)
        self.orig_start = self.convert_prop_tuple_list(robot_dom_prob.initialstate())
        self.grounded_robot_model_map = self.convert_domain_obj_map(robot_dom_prob)

        self.plan = []

        with open(plan_file) as p_fd:
            self.plan = ['_'.join(a.strip().split(' ')) for a in p_fd.readlines()]
       
        self.beh_trace = self.execute_plan()



    def convert_prop_tuple_list(self, orig_prop_list):
        prop_list = set()
        for p in orig_prop_list:
            #print (p)
            if type(p) is tuple:
                prop = '_'.join([str(i).lower() for i in p])
            else:
                prop = '_'.join([str(i).lower() for i in p.predicate])
            #print ("prop",prop)
            prop_list.add(prop)
        return prop_list



    def convert_domain_obj_map(self, prob_object):
        dom_map = {}
        dom_map['domain'] = {}
        ground_operator = self.ground_all_operators(prob_object)
        act_applied_preds = set()
        for act in ground_operator:
            sorted_var_name = list(act.variable_list.keys())
            sorted_var_name.sort()
            objs = [act.variable_list[k] for k in sorted_var_name]
            # Assume that the action names are created by combining act name and args by underscores
            action_name = act.operator_name + '_' + '_'.join(objs)
            dom_map['domain'][action_name] = {}
            dom_map['domain'][action_name]['precondition_pos'] = self.convert_prop_tuple_list(act.precondition_pos)
            dom_map['domain'][action_name]['precondition_pos_cond'] = set()
            dom_map['domain'][action_name]['precondition_neg'] = self.convert_prop_tuple_list(act.precondition_neg)
            dom_map['domain'][action_name]['effect_pos'] = self.convert_prop_tuple_list(act.effect_pos)
            dom_map['domain'][action_name]['effect_neg'] = self.convert_prop_tuple_list(act.effect_neg)
            dom_map['domain'][action_name]['effect_neg'].add("APPLIED_"+act.operator_name)
            act_applied_preds.add("APPLIED_"+act.operator_name)
            dom_map['domain'][action_name]['effect_pos_cond'] = set()
            dom_map['domain'][action_name]['effect_neg_cond'] = set()

        return dom_map

    def ground_all_operators(self, prob_object):
        ground_operators = []
        for act in prob_object.operators():
            ground_operators += list(prob_object.ground_operator(act))
        return ground_operators

    def execute_plan(self):
        print(self.grounded_robot_model_map)
        current_state = copy.deepcopy(self.orig_start)
        beh_trace = []
        l_id = 0
        for act in self.plan:
            precs = set()
            adds = set()
            dels = set()
            precs = self.grounded_robot_model_map['domain'][act]['precondition_pos']
            adds = self.grounded_robot_model_map['domain'][act]['effect_pos']
            dels = self.grounded_robot_model_map['domain'][act]['effect_neg']
            new_state = copy.deepcopy(current_state)
            new_state = (new_state | adds) - dels
            beh_trace.append(act +" "+ " ".join(list(new_state)))
            l_id += 1
        return beh_trace

    def get_beh_trace(self):
        return self.beh_trace

if __name__ == "__main__":
    dom = sys.argv[1]
    prob = sys.argv[2]
    plan = sys.argv[3]
    label = sys.argv[4]
    output_file = sys.argv[5]
    #spl_features = sys.argv[6]
    if len(prob.split('@')) > 1:
        spl_features = ' '.join(prob.split('@')[-1].split('#'))
    else:
        spl_features = ""

    exc = Executor(dom, prob, plan, label, spl_features)


    with open(output_file, 'w') as o_fd:
        o_fd.write("\n".join(exc.beh_trace)+"\n")
