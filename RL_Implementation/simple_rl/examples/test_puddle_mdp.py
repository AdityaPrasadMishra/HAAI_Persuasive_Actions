#!/usr/bin/env python

# Python imports.
from collections import defaultdict
import sys

# Other imports.
import srl_example_setup
from simple_rl.agents import QLearningAgent, RandomAgent
from simple_rl.agents.func_approx.LinearQAgentClass import LinearQAgent
from simple_rl.tasks import GridWorldMDP, GridWorldState
from simple_rl.run_experiments import run_agents_on_mdp 
# Two Puddles
from simple_rl.tasks.puddle.PuddleMDPClass import PuddleMDP
# Only Puddles #1
from simple_rl.tasks.puddle.PuddleMDPClass2 import PuddleMDP1
# Only Puddles #2
from simple_rl.tasks.puddle.PuddleMDPClass2 import PuddleMDP2
# No puddles
from simple_rl.tasks.puddle.PuddleMDPClass2 import PuddleMDP3


def main(open_plot=True):
    state_colors = defaultdict(lambda: defaultdict(lambda: "white"))
    state_colors[3][2] = "red"

    # Setup MDP, Agents.
    mdp = PuddleMDP()
    ql_agent = LinearQAgent(actions=mdp.get_actions(),num_features=2)
    mdp2 = PuddleMDP2()
    ql_agent2 = LinearQAgent(actions=mdp2.get_actions(),num_features=2)
    #rand_agent = RandomAgent(actions=mdp.get_actions())

    # Run experiment and make plot.
    run_agents_on_mdp([ql_agent], mdp, instances=15, episodes=1000, steps=40, open_plot=False)
    run_agents_on_mdp([ql_agent2], mdp2, instances=15, episodes=1000, steps=40, open_plot=False)

if __name__ == "__main__":
    main(open_plot=not sys.argv[-1] == "no_plot")

'''
state = mdp.get_init_state()
reward = 0
# Execute in MDP.
reward, next_state = mdp.execute_agent_action(action)

'''
