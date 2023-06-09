import os
import itertools
import linecache

from iqtree import iqtreeEvaluateTreesCommand
from print import printDictionary

def filterInitialTrees(msa_path: str):
        evaluate_command = iqtreeEvaluateTreesCommand(msa_path)
        os.system(evaluate_command)
        best_trees_dict = getBestTreesDictionary(msa_path)

        best_tree_numbers = dict(itertools.islice(best_trees_dict.items(), 5))

        print("Highest scoring likelihood trees:")

        printDictionary(best_tree_numbers)

        writeBestInitialTreesFile(best_tree_numbers)

def getBestTreesDictionary(msa_path: str) -> dict:
    file = msa_path + ".log"
    best_trees_dict = {}

    with open(file, "r") as fp:
        for line in fp:
            if line.startswith("Tree "):
                tree_line = line.split()
                tree = "Tree " + tree_line[1]
                score = float(tree_line[-1])
                best_trees_dict[tree] = score

    best_trees_dict = {k: v for k, v in sorted(best_trees_dict.items(), key=lambda item: item[1], reverse=True)}

    # print(best_trees_dict)

    return best_trees_dict

def writeBestInitialTreesFile(best_trees_number: dict):
    # needs refactoring
    file = "initial_trees.treefile"
    line_numbers = []
    lines = []
    dict_list = []

    for key in best_trees_number:
        dict_list.append(key[-1])

    for i in range(5):
        line_numbers.append(int(dict_list[i]))
        
    for i in line_numbers:
        x = linecache.getline(file, i).strip()
        lines.append(x)

    with open('initial_trees_best.treefile', 'w') as fp:
        for i in lines:
            fp.write("%s\n" % i)

    for i in range(5):
        j = str(i + 1)
        file_name = "initial_trees_best_" + j + ".treefile"

        with open(file_name, 'w') as fp:
            fp.write("%s\n" % lines[i])
