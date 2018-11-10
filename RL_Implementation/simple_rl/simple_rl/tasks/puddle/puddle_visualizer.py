# Python imports.
from __future__ import print_function
from collections import defaultdict
try:
    import pygame
except ImportError:
    print("Warning: pygame not installed (needed for visuals).")
import random
import sys
import numpy as np

# Other imports.
from simple_rl.planning import ValueIteration
from simple_rl.tasks import FourRoomMDP
from simple_rl.utils import mdp_visualizer as mdpv


def _draw_state(screen,
                pudd_mdp,
                state,
                policy=None,
                action_char_dict={},
                show_value=False,
                agent=None,
                draw_statics=False,
                agent_shape=None):
    '''
    Args:
        screen (pygame.Surface)
        pudd_mdp (MDP)
        state (State)
        show_value (bool)
        agent (Agent): Used to show value, by default uses VI.
        draw_statics (bool)
        agent_shape (pygame.rect)

    Returns:
        (pygame.Shape)
    '''
    # Make value dict.
    val_text_dict = defaultdict(lambda : defaultdict(float))
    if show_value:
        if agent is not None:
            # Use agent value estimates.
            for s in agent.q_func.keys():
                val_text_dict[s.x][s.y] = agent.get_value(s)
        else:
            # Use Value Iteration to compute value.
            vi = ValueIteration(pudd_mdp)
            vi.run_vi()
            for s in vi.get_states():
                val_text_dict[s.x][s.y] = vi.get_value(s)

    # Make policy dict.
    policy_dict = defaultdict(lambda : defaultdict(str))
    if policy:
        vi = ValueIteration(pudd_mdp)
        vi.run_vi()
        for s in vi.get_states():
            policy_dict[s.x][s.y] = policy(s)

    # Prep some dimensions to make drawing easier.
    scr_width, scr_height = screen.get_width(), screen.get_height()
    width_buffer = scr_width / 10.0
    height_buffer = 30 + (scr_height / 10.0) # Add 30 for title.
    cell_width = (scr_width - width_buffer * 2) / 10 #pudd_mdp.width
    cell_height = (scr_height - height_buffer * 2) / 10 # pudd_mdp.height
    goal_locs = pudd_mdp.get_goal_locs()
    # puddle_rects = pudd_mdp.get_puddle_rects()
    font_size = int(min(cell_width, cell_height) / 4.0)
    reg_font = pygame.font.SysFont("CMU Serif", font_size)
    cc_font = pygame.font.SysFont("Courier", font_size*2 + 2)
    delta = 0.2
    #print ("goal locs", goal_locs)
    # Draw the static entities.
    if draw_statics:
        # For each row:
        for i in np.linspace(0,1,11):
            # For each column:
            for j in np.linspace(0,1,11):
                #print ("i,j",i,j)

                top_left_point = width_buffer + cell_width*i*10, height_buffer + cell_height*j*10
                r = pygame.draw.rect(screen, (46, 49, 49), top_left_point + (cell_width, cell_height), 3)

                if pudd_mdp.is_puddle_location(i, j):
                    # Draw the walls.
                    #print ("True for ", i, j)
                    top_left_point = width_buffer + cell_width*(i*10) + 5, height_buffer + cell_height*j*10 + 5
                    r = pygame.draw.rect(screen, (0, 127, 255), top_left_point + (cell_width-10, cell_height-10), 0)

                if [min(i+delta,1.0),min(j+delta,1.0)] in goal_locs:
                    # Draw goal.
                    circle_center = int(top_left_point[0] + cell_width/2.0), int(top_left_point[1] + cell_height/2.0)
                    circler_color = (154, 195, 157)
                    pygame.draw.circle(screen, circler_color, circle_center, int(min(cell_width, cell_height) / 3.0))


                # Current state.
                if not show_value and (round(i,1),round(j,1)) == (round(state.x,1), round(state.y,1)) and agent_shape is None:
                    tri_center = int(top_left_point[0] + cell_width/2.0), int(top_left_point[1] + cell_height/2.0)
                    agent_shape = _draw_agent(tri_center, screen, base_size=min(cell_width, cell_height)/2.5 - 8)

#    if agent_shape is not None:
#        # Clear the old shape.
#        pygame.draw.rect(screen, (255,255,255), agent_shape)
#        top_left_point = width_buffer + cell_width*(state.x - 1), height_buffer + cell_height*(pudd_mdp.height - state.y)
#        tri_center = int(top_left_point[0] + cell_width/2.0), int(top_left_point[1] + cell_height/2.0)

        # Draw new.
#        agent_shape = _draw_agent(tri_center, screen, base_size=min(cell_width, cell_height)/2.5 - 8)

    pygame.display.flip()

    return agent_shape


def _draw_agent(center_point, screen, base_size=20):
    '''
    Args:
        center_point (tuple): (x,y)
        screen (pygame.Surface)

    Returns:
        (pygame.rect)
    '''
    tri_bot_left = center_point[0] - base_size, center_point[1] + base_size
    tri_bot_right = center_point[0] + base_size, center_point[1] + base_size
    tri_top = center_point[0], center_point[1] - base_size
    tri = [tri_bot_left, tri_top, tri_bot_right]
    tri_color = (98, 140, 190)
    return pygame.draw.polygon(screen, tri_color, tri)
