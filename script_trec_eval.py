# Example execution:
# > python script_trec_eval.py [GROUND_TRUTH_FILE_ADDRESS] [RESULT_FILE_ADDRESS] 

import subprocess
import sys

ground_truth = sys.argv[1]
results = sys.argv[2]
command = ["./trec_eval", "-m", "map", "-m", "P.10", "-m", "ndcg", ground_truth, results]
subprocess.run(command)