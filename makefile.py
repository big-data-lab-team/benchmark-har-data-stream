import subprocess
import sys
import math
import os
from statistics import mean

def mondrian_forest_command(tree_count):
    return ["-DCLASSIFIER_INITIALIZATION_FILE=\"mond.cpp\"", \
            "-DTREE_COUNT=" + str(tree_count), \
            "-o", "mondrian_l" + str(lifetime) + "_b" + str(base_measure) + "_d" + str(discount_factor) + "_t" + str(tree_count)]

def empty_classifier_command():
    return ["-DCLASSIFIER_INITIALIZATION_FILE=\"empty.cpp\"", \
            "-o", "empty_classifier"]

def rangy(mini, maxi, step):
    return [round(mini + x * step, 2) for x in range(0, math.floor((maxi-mini)/step))]

#Make all the binary
def compile():
    compilation_list = []

    OrpailleCC_DIR = "/home/magoa/phd/OrpailleCC"
    OrpailleCC_INC = OrpailleCC_DIR + "/src"

    base_compilation_command = ["g++", "-std=c++11", \
                                "-I" + OrpailleCC_INC,  "main.cpp", \
                                "-DLABEL_COUNT=2", "-DFEATURES_COUNT=3"]

    compilation_list.append(base_compilation_command + mondrian_forest_command(20))
    compilation_list.append(base_compilation_command + empty_classifier_command())
    # for  lifetime in rangy(0.5, 3.0, 0.1):
        # for  base in rangy(0.0, 1.0, 0.1):
            # for d in rangy(0.1, 2.0, 0.1):
                # compilation_list.append(base_compilation_command + mondrian_forest_command(lifetime, base, d, 20))

    for command in compilation_list:
        print(" ".join(command))
        command_result = subprocess.call(command)

def extract_features(window):
    starting_index = 2
    window_transposed = [[float(i) for i in x] for x in zip(*window)]

    features = []
    for i in range(2, 5):
        features.append(max(window_transposed[i]))
        features.append(min(window_transposed[i]))
        features.append(mean(window_transposed[i]))
    #Extract the most frequent label in the window and use it as the label for the data point.
    features.append(max(set(window_transposed[-1]), key = window_transposed[-1].count))
    return [str(i) for i in features]

def process_file(in_f, out_f, window_size):
    window = []
    for line in in_f:
        window.append(line.split("\t"))
        if len(window) >= window_size:
            features = extract_features(window)
            window = []
            out_f.write("\t".join(features) + "\n")

#Build the dataset
def dataset():
    output_directory = "/tmp/"
    filenames = ["subject1_ideal.log"]
    for filename in filenames:
        try:
            in_f = open(filename,"r")
            output_filename = output_directory + \
                                "processed_" + \
                                os.path.basename(filename)
            out_f = open(output_filename,"w")
            process_file(in_f, out_f, 10)
        except IOError:
            print("Could not open file: " + filename)
    return

if len(sys.argv) > 1:
    if sys.argv[1] == "compile":
        compile()
    if sys.argv[1] == "dataset":
        dataset()

