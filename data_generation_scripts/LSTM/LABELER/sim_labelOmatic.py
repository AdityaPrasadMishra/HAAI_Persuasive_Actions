import sys

robot_plan_file = sys.argv[1]
human_plan_file = sys.argv[2]
label_file = sys.argv[3]

fetch_box_seq = []
unfetc_box_seq = []
label_seq = []

curr_fetch_block = True
curr_unfetch_block = False

with open(robot_plan_file) as r_fd:
    robot_plan = [r.strip() for r in r_fd.readlines()]

with open(human_plan_file) as h_fd:
    human_plan = [h.strip() for h in h_fd.readlines()]


for act in human_plan:
    if curr_unfetch_block:
        unfetc_box_seq.append(act)
    elif curr_fetch_block:
        fetch_box_seq.append(act)
        if act.split(" ")[0] == "fetch_box":
            curr_fetch_block = False
            curr_unfetch_block = True

curr_fetch_block = True
curr_unfetch_block = False
other_block = False
human_plan_finished = False
human_plan_id = 0
for act in robot_plan:
    #print (act, human_plan[human_plan_id],curr_fetch_block,curr_unfetch_block,other_block)
    if human_plan_finished:
        #print ("act",act, human_plan_id, human_plan[human_plan_id])
        if act.split(" ")[0] == "unfetch_box":
            label_seq.append("EXP")
        else:
            label_seq.append("UNEXP")
    elif other_block:
        if act == human_plan[human_plan_id]:
            label_seq.append("EXP")
            human_plan_id += 1
            #print ("We reached here")
        else:
            label_seq.append("UNEXP")
    elif curr_unfetch_block:
        #print ("act",act, human_plan_id, human_plan[human_plan_id])
        if act.split(" ")[0] == "unfetch_box":
            label_seq.append("EXP")
            other_block = True
            curr_unfetch_block = False
            while human_plan[human_plan_id].split(" ")[0] != "unfetch_box":
                human_plan_id += 1
            human_plan_id += 1
        elif act == human_plan[human_plan_id]:
            label_seq.append("EXP")
            human_plan_id += 1
        else:
            label_seq.append("EXP")

    elif curr_fetch_block:
        #print ("act",act, human_plan_id, human_plan[human_plan_id].split(" ")[0] != "fetch_box")
        if act.split(" ")[0] == "fetch_box":
            label_seq.append("EXP")
            curr_fetch_block = False
            curr_unfetch_block = True
            while human_plan[human_plan_id].split(" ")[0] != "fetch_box":
                human_plan_id += 1
            human_plan_id += 1

        elif act == human_plan[human_plan_id]:
            label_seq.append("EXP")
            human_plan_id += 1
        else:
            label_seq.append("EXP")
    if human_plan_id >= len(human_plan):
        human_plan_finished = True


with open(label_file, 'w') as l_fd:
    l_fd.write("\n".join(label_seq)+"\n")
