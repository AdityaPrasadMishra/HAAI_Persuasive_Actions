import pddlpy
import sys
import copy

OBSX_PREFIX = "observedx_"
OBSY_PREFIX = "observedy_"

class Executor:

    def __init__(self, robot_domain_model, robot_problem, plan_file, label_file, spl_features, feat_x, feat_y):
        robot_dom_prob = pddlpy.DomainProblem(robot_domain_model, robot_problem)
        self.orig_start = self.convert_prop_tuple_list(robot_dom_prob.initialstate())
        self.grounded_robot_model_map = self.convert_domain_obj_map(robot_dom_prob)
        self.explain_x = feat_x
        self.explain_y = feat_y
        self.spl_features = spl_features
        self.plan = []
        self.label_seq = []

        with open(plan_file) as p_fd:
            self.plan = ['_'.join(a.strip().split(' ')) for a in p_fd.readlines()]
        with open(label_file) as l_fd:
            self.label_seq = [l.strip() for l in l_fd.readlines()]
       
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
        current_state = copy.deepcopy(self.orig_start)
        beh_trace = []
        l_id = 0
        obs_x = OBSX_PREFIX + self.explain_x
        obs_y = OBSY_PREFIX + self.explain_y

        for act in self.plan:
            precs = set()
            adds = set()
            dels = set()
            precs = self.grounded_robot_model_map['domain'][act]['precondition_pos']
            adds = self.grounded_robot_model_map['domain'][act]['effect_pos']
            dels = self.grounded_robot_model_map['domain'][act]['effect_neg']
            new_state = copy.deepcopy(current_state)
            new_state = (new_state | adds) - dels
            #beh_trace.append(act +" "+ " ".join(list(new_state)) +" " + self.spl_features+ " "+ self.label_seq[l_id])
            pair_feats = ""
            if obs_x in new_state:
                pair_feats += " same_observationx"
            if obs_y in new_state:
                pair_feats += " same_observationy"

            beh_trace.append(act +" " + self.spl_features+pair_feats+ " "+ self.label_seq[l_id])
            l_id += 1
        return beh_trace


if __name__ == "__main__":
    dom = sys.argv[1]
    prob = sys.argv[2]
    plan = sys.argv[3]
    label = sys.argv[4]
    output_file = sys.argv[5]
    #spl_features = sys.argv[6]
    if len(prob.split('@')) > 1:
        spl_features = ' '.join(prob.split('@')[-1].split('#'))
        tmp_feats = prob.split('@')[-1].split('#')
        feat_x = tmp_feats[0].split('_')[-1]
        feat_y = tmp_feats[1].split('_')[-1]
    else:
        spl_features = ""
        feat_x = ""
        feat_y = ""

    print ("feat_x",feat_x,feat_y)

    exc = Executor(dom, prob, plan, label, spl_features, feat_x, feat_y)


    with open(output_file, 'w') as o_fd:
        o_fd.write("\n".join(exc.beh_trace)+"\n")
