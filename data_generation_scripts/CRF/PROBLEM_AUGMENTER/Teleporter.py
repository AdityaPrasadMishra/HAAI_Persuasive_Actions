import sys
import numpy
import os
import time

__FD_PLAN_CMD__ = "./fdplan.sh {} {}"


prob_file = sys.argv[1]
templ_file = sys.argv[2]
dest_dir = sys.argv[3]

SAMPLE_COUNT = 500

X_DIM = ['x0','x1', 'x2']
Y_DIM = ['y0','y1', 'y2']
epsilon = 0.5



with open(templ_file) as t_fd:
    templ_str = t_fd.read()

    rand_obj = numpy.random.RandomState()

EXPL_ACT = False
for i in range(SAMPLE_COUNT):
    rand_obj.seed()
    start_x = rand_obj.choice(X_DIM,size=1)[0]
    rand_obj.seed()
    rand_obj = numpy.random.RandomState()
    start_y = rand_obj.choice(Y_DIM,size=1)[0]
    rand_obj.seed()
    rand_obj = numpy.random.RandomState()
    obs_x = rand_obj.choice(X_DIM,size=1)[0]
    rand_obj.seed()
    rand_obj = numpy.random.RandomState()
    obs_y = rand_obj.choice(Y_DIM,size=1)[0]
    rand_obj.seed()
    rand_obj = numpy.random.RandomState()
    box_x = rand_obj.choice(X_DIM,size=1)[0]
    rand_obj.seed()
    rand_obj = numpy.random.RandomState()
    box_y = rand_obj.choice(Y_DIM,size=1)[0]
    rand_obj.seed()
    rand_obj = numpy.random.RandomState()
    unload_x = rand_obj.choice(X_DIM,size=1)[0]
    rand_obj.seed()
    rand_obj = numpy.random.RandomState()
    unload_y = rand_obj.choice(Y_DIM,size=1)[0]

    
#    if numpy.random.random() < epsilon:
#        EXPL_ACT = True
#    else:
#        EXPL_ACT = False

#    if EXPL_ACT:
#        rand_obj.seed()
#        rand_obj = numpy.random.RandomState()
#        exp_obs_x = rand_obj.choice(X_DIM,size=1)[0]
#        rand_obj.seed()
#        rand_obj = numpy.random.RandomState()
#        exp_obs_y = rand_obj.choice(Y_DIM,size=1)[0]
#        expl_str = "@explain_"+exp_obs_x+"#"+"explain_"+exp_obs_y
#    else:
    expl_str = ""



    new_dst_file = dest_dir+"prob"+str(start_x)+"_"+str(start_y)+"_"+box_x+"_"+box_y+"_"+unload_x+"_"+unload_y+"_"+str(obs_x)+"_"+str(obs_y)+expl_str
    new_human_dst_file = dest_dir+"human_prob"+str(start_x)+"_"+str(start_y)+"_"+box_x+"_"+box_y+"_"+unload_x+"_"+unload_y+"_"+str(obs_x)+"_"+str(obs_y)+expl_str

    start_loc_preds = "(currentx {})\n(currenty {})".format(start_x,start_y)
    box_loc_preds = "(boxx {})\n(boxy {})".format(box_x,box_y)
    unload_loc_preds = "(unloadboxx {})\n(unloadboxy {})".format(unload_x,unload_y)
    obs_loc_preds = "(observedx {})\n(observedy {})".format(obs_x,obs_y)

    if EXPL_ACT:
        expl_obs_loc_preds = "(observedx {})\n(observedy {})".format(exp_obs_x,exp_obs_y)
    else:
        expl_obs_loc_preds = ""



    with open(new_dst_file, 'w') as d_fd:
        d_fd.write(templ_str.format(start_loc_preds,box_loc_preds,unload_loc_preds,obs_loc_preds))


    with open(new_human_dst_file, 'w') as d_fd:
        d_fd.write(templ_str.format(start_loc_preds,box_loc_preds,unload_loc_preds,expl_obs_loc_preds))


#    exp_obs_x = obs_x
#    exp_obs_y = obs_y
    for exp_obs_x in X_DIM:
        for exp_obs_y in Y_DIM:
            expl_str = "@explain_"+exp_obs_x+"#"+"explain_"+exp_obs_y

            new_dst_file = dest_dir+"prob"+str(start_x)+"_"+str(start_y)+"_"+box_x+"_"+box_y+"_"+unload_x+"_"+unload_y+"_"+str(obs_x)+"_"+str(obs_y)+expl_str
            new_human_dst_file = dest_dir+"human_prob"+str(start_x)+"_"+str(start_y)+"_"+box_x+"_"+box_y+"_"+unload_x+"_"+unload_y+"_"+str(obs_x)+"_"+str(obs_y)+expl_str

            start_loc_preds = "(currentx {})\n(currenty {})".format(start_x,start_y)
            box_loc_preds = "(boxx {})\n(boxy {})".format(box_x,box_y)
            unload_loc_preds = "(unloadboxx {})\n(unloadboxy {})".format(unload_x,unload_y)
            obs_loc_preds = "(observedx {})\n(observedy {})".format(obs_x,obs_y)

            expl_obs_loc_preds = "(observedx {})\n(observedy {})".format(exp_obs_x,exp_obs_y)



            with open(new_dst_file, 'w') as d_fd:
                d_fd.write(templ_str.format(start_loc_preds,box_loc_preds,unload_loc_preds,obs_loc_preds))


            with open(new_human_dst_file, 'w') as d_fd:
                d_fd.write(templ_str.format(start_loc_preds,box_loc_preds,unload_loc_preds,expl_obs_loc_preds))

#    rand_obj.seed()
#    rand_obj = numpy.random.RandomState()
#    exp_obs_x = rand_obj.choice(X_DIM,size=1)[0]
#    rand_obj.seed()
#    rand_obj = numpy.random.RandomState()
#    exp_obs_y = rand_obj.choice(Y_DIM,size=1)[0]
#    expl_str = "@explain_"+exp_obs_x+"#"+"explain_"+exp_obs_y



#    expl_str = "@explain_"+exp_obs_x+"#"+"explain_"+exp_obs_y
#    print (expl_str)
#    new_dst_file = dest_dir+"prob"+str(start_x)+"_"+str(start_y)+"_"+box_x+"_"+box_y+"_"+unload_x+"_"+unload_y+"_"+str(obs_x)+"_"+str(obs_y)+expl_str
#    new_human_dst_file = dest_dir+"human_prob"+str(start_x)+"_"+str(start_y)+"_"+box_x+"_"+box_y+"_"+unload_x+"_"+unload_y+"_"+str(obs_x)+"_"+str(obs_y)+expl_str

#    start_loc_preds = "(currentx {})\n(currenty {})".format(start_x,start_y)
#    box_loc_preds = "(boxx {})\n(boxy {})".format(box_x,box_y)
#    unload_loc_preds = "(unloadboxx {})\n(unloadboxy {})".format(unload_x,unload_y)
#    obs_loc_preds = "(observedx {})\n(observedy {})".format(obs_x,obs_y)

#    expl_obs_loc_preds = "(observedx {})\n(observedy {})".format(exp_obs_x,exp_obs_y)

    

#    with open(new_dst_file, 'w') as d_fd:
#        d_fd.write(templ_str.format(start_loc_preds,box_loc_preds,unload_loc_preds,obs_loc_preds))


#    with open(new_human_dst_file, 'w') as d_fd:
#        d_fd.write(templ_str.format(start_loc_preds,box_loc_preds,unload_loc_preds,expl_obs_loc_preds))





