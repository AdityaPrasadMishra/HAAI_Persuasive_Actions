import argparse
import sys
import time
from Problem import *

def main():
    parser = argparse.ArgumentParser(description='''The driver Script for the Explanation generation''',
                                     epilog="Usage >> ./Explainer.py -d ../test_domain/original_domain.pddl -p" +
                                            " ../test_domain/original_problem.pddl -f ../test_domain/plan_file -e ../test_domain/explanation_actions -m 2")
    '''
        # Flags
        --generate_lattice
    '''

    parser.add_argument('-d', '--domain_model',   type=str, help="Domain file with real PDDL model of robot.", required=True)
    parser.add_argument('-p', '--problem', type=str, help="Problem file for robot.", required=True)
    parser.add_argument('-f', '--plan_file', type=str, help="Plan file for robot.", required=True)
    parser.add_argument('-e', '--explanatory_actions_file', type=str, help="Explanatory actions", required=True)
    parser.add_argument('-m', '--max_length', type=str, help="Max length", required=True)



    if not sys.argv[1:] or '-h' in sys.argv[1:]:
        print (parser.print_help())
        sys.exit(1)
    args = parser.parse_args()
    

    problem = Problem(args.domain_model, args.problem, args.plan_file, args.explanatory_actions_file, int(args.max_length))
    st_time = time.time()
    pl = problem.explain()
    print ("Explanation",pl)
    print ("Explanation Size >>>",len(pl))
    print ("Total time >>>",time.time() - st_time)

if __name__ == "__main__":
    main()
