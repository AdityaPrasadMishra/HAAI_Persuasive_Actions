import pddlpy
import sys
import copy

OBSX_PREFIX = "observedx_"
OBSY_PREFIX = "observedy_"

class Executor:

    def __init__(self, robot_domain_model, robot_problem, plan_file):
        robot_dom_prob = pddlpy.DomainProblem(robot_domain_model, robot_problem)
        self.orig_start = self.convert_prop_tuple_list(robot_dom_prob.initialstate())
        self.goal = self.convert_prop_tuple_list(robot_dom_prob.goals())
        self.grounded_robot_model_map = self.convert_domain_obj_map(robot_dom_prob)
        self.plan = []
        self.label_seq = []

        with open(plan_file) as p_fd:
            self.plan = [' '.join(a.strip().split(' ')) for a in p_fd.readlines()]
       
        self.action_names = list(self.grounded_robot_model_map['domain'].keys())
        #print (self.action_names)

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
            action_name = act.operator_name + ' ' + ' '.join(objs)
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

    def execute_plan(self, feat_x, feat_y):
        self.explain_x = feat_x
        self.explain_y = feat_y

        current_state = copy.deepcopy(self.orig_start)
        action_types = ['move_righty','move_lefty','move_topx','move_bottomx','fetch_box','unfetch_box','waiting']
        beh_trace = []
        l_id = 0
        obs_x = OBSX_PREFIX + self.explain_x
        obs_y = OBSY_PREFIX + self.explain_y

        box_feats = []
        goal_feats = []
        explain_feats = []

        #print ("self.orig_start",self.orig_start)
        boxx_feat_found = False

        boxx_pred = None
        boxy_pred = None
        unloadboxx_pred = None
        unloadboxy_pred = None
        observedx_pred = None
        observedy_pred = None

        for pred in self.orig_start:
            if "boxx_x" in pred:
                boxx_pred = pred
            elif "boxy_y" in pred:
                boxy_pred = pred
            elif "unloadboxx_x" in pred:
                unloadboxx_pred = pred
            elif "unloadboxy_y" in pred:
                unloadboxy_pred = pred
        for pred in self.goal:
            if "observedx_x" in pred:
                observedx_pred = pred
            elif "observedy_y" in pred:
                observedy_pred = pred




        unloadboxx_feat_found = False
        unloadboxy_feat_found = False
        observedx_feat_found = False
        observedy_feat_found = False

        unloadboxx_feat = None
        unloadboxy_feat = None
        observedx_feat = None
        observedy_feat = None



        if self.explain_x == "":
            explain_x_feat = format(0, '03b')
        else:
            explain_x_feat = format(int(self.explain_x[-1]), '03b')

        if self.explain_y == "":
            explain_y_feat = format(0, '03b')
        else:
            explain_y_feat =  format(int(self.explain_y[-1]), '03b') 

        explain_feats = [explain_x_feat] + [explain_y_feat]

        beh_trace.append(" ".join(self.orig_start))

        for act in self.plan:
            curr_feats = []
            precs = set()
            adds = set()
            dels = set()
            precs = self.grounded_robot_model_map['domain'][act]['precondition_pos']
            adds = self.grounded_robot_model_map['domain'][act]['effect_pos']
            dels = self.grounded_robot_model_map['domain'][act]['effect_neg']
            #print (current_state)
            #print ("adds",adds)
            #print ("dels",dels)
            new_state = copy.deepcopy(current_state)
            new_state = (new_state | adds) - dels
            currentx_feat_found = False
            currentx_feat = None
            currenty_feat_found = False
            currenty_feat = None

            for pred in new_state:
                if not currentx_feat_found:
                    if "currentx_x" in pred:
                        currentx_feat = pred
                        currentx_feat_found = True
                if not currenty_feat_found:
                    if "currenty_y" in pred:
                        currenty_feat = pred
                        currenty_feat_found = True
            #curr_feats = [currentx_feat] + [currenty_feat]


            if "unfetched_box" in new_state:
                unfetch_feat = "Unfetch"
            else:
                unfetch_feat = ""

            if "fetched_box" in new_state:
                fetch_feat = "fetch"
            else:
                #print ("fetched box is missing")
                fetch_feat = ""

            spl_expl_feature = currentx_feat+"_"+currenty_feat+"_"+self.explain_x+"_"+self.explain_y+"_"+unfetch_feat+"_"+fetch_feat 
            beh_trace.append(act + " " + " ".join(list(new_state))+" "+spl_expl_feature+" "+self.explain_x+" "+self.explain_y)

            l_id += 1
            #print (new_state)
            current_state = copy.deepcopy(new_state)
        beh_trace.append(" ".join(current_state)+" GOAL_COMPLETED")
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

    exc = Executor(dom, prob, plan, spl_features, feat_x, feat_y, label)


    with open(output_file, 'w') as o_fd:
        o_fd.write("\n".join(exc.beh_trace)+"\n")
