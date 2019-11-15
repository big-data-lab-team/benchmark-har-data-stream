import subprocess
import sys
import math
import os
from statistics import mean

def rangy(mini, maxi, step):
    return [round(mini + x * step, 2) for x in range(0, math.floor((maxi-mini)/step))]

#Make all the binary
def compile():
    subprocess.call(["make"])

def latex():
    subprocess.call(["make"], cwd="paper/")

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
    if sys.argv[1] == "latex":
        latex()

