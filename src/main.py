#!/usr/bin/env python3

import argparse
import os
import time
import traceback

from datetime import datetime
from multiprocessing import cpu_count

from filter_initial_trees import filterInitialTrees
from generate_initial_trees import generateInitialTrees
from generate_initial_trees import writeInitialTrees
from refine_trees import refineInitialTrees
from print import printHeader
from print import printSoftwareConfig

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--msa', type=str, help='input MSA in Phylp/Fasta/Nexus/Clustal format', required=True)
PARSER.add_argument('--init-trees', type=int, help='the number of initial trees generated', default=100)
PARSER.add_argument('--init-software', type=str, help='software used to generate initial trees', default='mpboot')
PARSER.add_argument('--ml-software', type=str, help='software used to generate ML trees', default='iqtree')

args = vars(PARSER.parse_args())
MSA_PATH = args['msa']
INIT_TREE_SIZE = args['init_trees']
INIT_SOFTWARE = args['init_software']
ML_SOFTWARE = args['ml_software']
TIMESTAMP = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

def main():
    try:
        initial_trees = []
        available_processors = cpu_count()

        program_start = time.time()

        printHeader()
        printSoftwareConfig(INIT_SOFTWARE, MSA_PATH, INIT_TREE_SIZE, ML_SOFTWARE, TIMESTAMP)

        # currently only uses MPBoot
        print("Generating initial {} initial trees using {} processors".format(INIT_TREE_SIZE, available_processors))
        initial_trees = generateInitialTrees(INIT_SOFTWARE, MSA_PATH, INIT_TREE_SIZE)
        writeInitialTrees(initial_trees)

        # uses IQ-Tree to filter initial trees based on likelihood scores
        print("Obtaining the best {} initial trees".format("5"))
        filterInitialTrees(MSA_PATH)

        # refine initial trees using maximum likelihood
        refineInitialTrees(MSA_PATH)

        program_end = time.time()

        runtime = program_end - program_start
        print("")
        print("Wall-clock time : ", time.strftime("%H:%M:%S", time.gmtime(runtime)))

        # remove old files
        os.system("rm tree.* initial_trees_* initial_trees.treefile best_tree.treefile parsimony.treefile")
            
    except Exception as err:
        print(f"Unexpected {err}, {type(err)}")
        traceback.print_tb(err.__traceback__)
        exit(1)

if __name__ == "__main__":
    main()