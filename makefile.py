import subprocess
import sys
import math
import os
import csv
import random
import statistics, re
import pandas as pd
import seaborn as sns
from statistics import mean 
import matplotlib.pyplot as plt
from random import shuffle
def stdev(l):
    if len(l) <= 1:
        return 0.0
    return statistics.stdev(l)
def hashStringToColor(string):
    hsh = hash(string)
    r = (hsh & 0xFF0000) >> 16
    g = (hsh & 0x00FF00) >> 8
    b = hsh & 0x0000FF
    return "#" + format(r, "02x") + format(g, "02x") + format(b, "02x")

def rangy(mini, maxi, step):
    return [round(mini + x * step, 2) for x in range(0, math.floor((maxi-mini)/step))]

#Make all the binary
def compile():
    subprocess.call(["make"])

def latex():
    subprocess.call(["make"], cwd="paper/")

#Build the dataset
def dataset_banos():
    # output_directory = "recofit/windowed_6/"
    # input_directory = "recofit/"
    ids = [3, 13, 15, 17, 23, 28, 31, 62, 64, 66, 67, 69, 71, 72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 84, 201, 203, 216, 218, 223, 224, 228, 229, 230, 231, 232, 233, 235, 236, 238, 239, 240, 241, 242, 244, 246, 247, 248, 252, 253, 454, 502, 506, 509, 512, 517, 525, 526, 528, 530, 531, 532, 533, 534, 535, 536, 537, 539, 541, 542, 543, 545, 546, 547, 549, 550, 551, 555, 556, 559, 560, 561, 564, 567, 570, 575, 576, 579, 590, 10001, 10002, 10003, 10004, 10005, 10006]
    filenames = ["subject_" + str(i) + ".log" for i in ids]
    input_directory = "recofit/svg/"
    output_directory = "recofit/windowed_histogramm_6/"
    # ids = [i for i in range(1, 18)]
    # filenames = ["subject" + str(i) + "_ideal.log" for i in ids]
    for filename in filenames:
        try:
            in_f = open(input_directory + filename,"r")
            output_filename = output_directory + \
                                "processed_" + \
                                os.path.basename(filename)
            out_f = open(output_filename,"w")
            process_file(in_f, out_f, 50, True)
            print(filename)
        except IOError:
            print("Could not open file: " + filename)
    return

def process_file(in_f, out_f, window_size, histogram=False):
    window = []
    a = 0
    for line in in_f:
        window.append(line.split("\t"))
        if len(window) >= window_size:
            a = a+1
            if histogram:
                features = extract_histogram(window)
            else:
                features = extract_features(window)
            window = []
            out_f.write("\t".join(features) + "\n")

def extract_features(window):
    starting_index = 2
    window_transposed = [[float(i) if i != "" else 0.0 for i in x] for x in zip(*window)]

    features = []
    for i in range(2, 8):
        features.append(mean(window_transposed[i]))
        features.append(stdev(window_transposed[i]))
    #Extract the most frequent label in the window and use it as the label for the data point.
    features.append(max(set(window_transposed[-1]), key = window_transposed[-1].count))
    return [str(i) for i in features]

def extract_histogram(window):
    bin_count = 20
    bin_range = 32 #±16
    bin_step = bin_range / bin_count
    starting_index = 2
    window_transposed = [[float(i) if i != "" else 0.0 for i in x] for x in zip(*window)]

    features = []
    for i in range(2, 8):
        bins = [0 for j in range(bin_count)]
        shift = [x + (bin_range/2) for x in window_transposed[i] if x >= -(bin_range/2) and x < (bin_range/2)]
        loutre = [int((x - (x%bin_step))/bin_step) for x in shift]
        for j in loutre:
            bins[j] += 1
        bins = [x/len(window) for x in bins]

        features.extend(bins)
    #Extract the most frequent label in the window and use it as the label for the data point.
    features.append(max(set(window_transposed[-1]), key = window_transposed[-1].count))
    return [str(i) for i in features]

model_hashes = {}

def get_model_id(model_name):
    if model_name not in model_hashes:
        model_hashes[model_name] = str(len(model_hashes))
    return model_hashes[model_name]

def write_model_ids(filename):
    f = open(filename, "w")
    for key, value in model_hashes.items():
        f.write(value + "," + key + "\n")
def calibration_list(commands):
    for filename in ["processed_subject1_ideal_shuf.log"]:
        for run_id in map(str,range(10)):
            seed = str(random.randint(0, 2**24))
            model_id = get_model_id("Empty," + filename)
            commands.append(["bin/banos_6/empty_classifier", filename, seed, model_id, run_id])
            for cluster in ["10", "20", "32", "33", "34", "40", "50"]:
                for error_th in ["2", "4", "8", "10", "16"]:
                    for cleaning in ["0", "1", "2"]:
                        if cleaning == "0":
                            model_id = get_model_id("MCNN," + filename + "," + cluster + "," + error_th + "," + cleaning + ",10")
                            commands.append(["bin/banos_6/mcnn_c" + cluster, filename, seed, model_id, run_id, error_th, cleaning, "10"])
                        else:
                            for performance_th in ["10", "30", "50", "70", "90"]:
                                model_id = get_model_id("MCNN," + filename + "," + cluster + "," + error_th + "," + cleaning + "," + performance_th)
                                commands.append(["bin/banos_6/mcnn_c" + cluster, filename, seed, model_id, run_id, error_th, cleaning, performance_th])

            # for hidden_layer_size in ["1", "3", "5", "7", "9", "11"]:
                # for learning_rate in ["0.01", "0.05", "0.1", "0.15", "0.2"]:
                    # model_id = get_model_id("MLP," + filename + "," + learning_rate + ",3," + hidden_layer_size)
                    # commands.append(["bin/banos/mlp_3", filename, seed, model_id, run_id, learning_rate, hidden_layer_size])


            for confidence in ["0.01"]:
                for grace_period in ["10"]:
                    for adaptive in ["0", "1"]:
                        model_id = get_model_id("StreamDM HoeffdingTree," + filename + "," + adaptive + "," + confidence + "," + grace_period)
                        commands.append(["bin/banos_6/streamdm_ht", filename, seed, model_id, run_id, adaptive, confidence, grace_period])

            for base_count in ["0.0", "0.01", "0.05", "0.005", "0.1", "0.3", "0.5", "0.8", "1.0", "1.3"]:
                for budget in ["2.0", "1.6", "1.0", "1.4", "0.8", "0.6", "0.4", "0.2"]:
                    for discount in ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]:
                        for tree_count in [1, 5, 20, 10, 50]:
                            model_id = get_model_id("Mondrian," + filename + "," + budget + "," + base_count + "," + discount + "," + str(tree_count) + ",600000")
                            commands.append(["bin/banos_6/mondrian_t" + str(tree_count), filename, seed, model_id, run_id, budget, base_count, discount])


def final_list(commands):
    repetition_count = 30
    ####### Controlling the datasets: To add a dataset, both add it here and to the setup. ########
    #for dataset_name in ["banos_3"]:
    for dataset_name in ["banos_6", "banos_6_v1", "banos_6_v2", "banos_6_v3", "banos_6_v4", "banos_6_v5", "banos_6_v6", "recofit_6"]:
    #for dataset_name in ["dataset_3", "dataset_2", "dataset_1", "banos_3", "recofit_3", "drift_3", "banos_6", "recofit_6", "drift_6"]:
        filename = "tmp/" + dataset_name + ".log"
        for run_id in map(str,range(repetition_count)):
            seed = str(run_id)
#            model_id = get_model_id("Empty," + filename)
#            commands.append(["bin/" + dataset_name + "/empty_classifier", filename, seed, model_id, run_id])
#            model_id = get_model_id("MCNN," + filename + ",10,16,0,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c10", filename, seed, model_id, run_id, "2", "0", "10"])
#            model_id = get_model_id("MCNN," + filename + ",20,10,0,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c20", filename, seed, model_id, run_id, "10", "0", "10"])
#            model_id = get_model_id("MCNN," + filename + ",40,8,0,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c40", filename, seed, model_id, run_id, "8", "0", "10"])
#            model_id = get_model_id("MCNN," + filename + ",33,16,0,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c33", filename, seed, model_id, run_id, "16", "0", "10"])
#            model_id = get_model_id("MCNN," + filename + ",50,2,0,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c50", filename, seed, model_id, run_id, "2", "0", "10"])

#            model_id = get_model_id("MCNN," + filename + ",10,2,1,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c10", filename, seed, model_id, run_id, "2", "1", "10"])
#            model_id = get_model_id("MCNN," + filename + ",20,10,1,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c20", filename, seed, model_id, run_id, "10", "1", "10"])
#            model_id = get_model_id("MCNN," + filename + ",40,8,1,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c40", filename, seed, model_id, run_id, "8", "1", "10"])
#            model_id = get_model_id("MCNN," + filename + ",33,16,1,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c33", filename, seed, model_id, run_id, "16", "1", "10"])
#            model_id = get_model_id("MCNN," + filename + ",50,2,1,10")
#            commands.append(["bin/" + dataset_name + "/mcnn_c50", filename, seed, model_id, run_id, "2", "1", "10"])

            model_id = get_model_id("Mondrian," + filename + ",1.0,0.1,1.0,1,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t1", filename, seed, model_id, run_id, "1.0", "0.0", "1.0"])
            model_id = get_model_id("Mondrian," + filename + ",0.4,0.0,1.0,5,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t5", filename, seed, model_id, run_id, "0.4", "0.0", "1.0"])
            model_id = get_model_id("Mondrian," + filename + ",0.4,0.0,1.0,10,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t10", filename, seed, model_id, run_id, "0.4", "0.0", "1.0"])
            model_id = get_model_id("Mondrian," + filename + ",0.2,0.0,1.0,50,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t50", filename, seed, model_id, run_id, "0.2", "0.0", "1.0"])
            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.1,1.0,1,1200000')
            commands.append(['bin/' + dataset_name + '/mondrian_t1_double', filename, seed, model_id, run_id, '0.8', '0.1', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.0,1.0,5,1200000')
            commands.append(['bin/' + dataset_name + '/mondrian_t5_double', filename, seed, model_id, run_id, '0.8', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,1.0,10,1200000')
            commands.append(['bin/' + dataset_name + '/mondrian_t10_double', filename, seed, model_id, run_id, '0.6', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,0.1,50,1200000')
            commands.append(['bin/' + dataset_name + '/mondrian_t50_double', filename, seed, model_id, run_id, '0.6', '0.0', '0.1'])
#            model_id = get_model_id("StreamDM HoeffdingTree," + filename + ",0,0.01,10")
#            commands.append(["bin/" + dataset_name + "/streamdm_ht", filename, seed, model_id, run_id, "0", "0.01", "10"])
#            model_id = get_model_id("NaiveBayes," + filename)
#            commands.append(["bin/" + dataset_name + "/naive_bayes", filename, seed, model_id, run_id])
#            model_id = get_model_id("StreamDM NaiveBayes," + filename)
#            commands.append(["bin/" + dataset_name + "/streamdm_naive_bayes", filename, seed, model_id, run_id])

            model_id = get_model_id('Mondrian,' + filename + ',1.0,0.0,1.0,1,3000000')
            commands.append(['bin/' + dataset_name + '/mondrian_t1_quintuple', filename, seed, model_id, run_id, '1.0', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.4,0.0,1.0,5,3000000')
            commands.append(['bin/' + dataset_name + '/mondrian_t5_quintuple', filename, seed, model_id, run_id, '0.4', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.4,0.0,1.0,10,3000000')
            commands.append(['bin/' + dataset_name + '/mondrian_t10_quintuple', filename, seed, model_id, run_id, '0.4', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.2,0.0,1.0,50,3000000')
            commands.append(['bin/' + dataset_name + '/mondrian_t50_quintuple', filename, seed, model_id, run_id, '0.2', '0.0', '1.0'])

    for dataset_name in ["banos_3_histogram", "banos_6_histogram"]:
        filename = "tmp/" + dataset_name + ".log"
        for run_id in map(str,range(1)):
            seed = str(random.randint(0, 2**24))
            model_id = get_model_id("FNN," + filename + ",0.1,30")
            commands.append(["bin/" + dataset_name + "/mlp_3", filename, seed, model_id, run_id, "0.1", "weights_" + dataset_name, "30"])

# for the purposes of trying out only Mondrian trees, the "run" option should be chosen
def run(output_filename, run_output_filename, calibration=False):
    output_file = open(output_filename, "w")
    run_output_file = open(run_output_filename, "w")
    commands = []
    if calibration:
        calibration_list(commands)
    else:
        final_list(commands)

    shuffle(commands)

    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    write_model_ids(OUTDIR+"/models.csv")

    #Run every commands
    for i, command in enumerate(commands):
        print(" ".join(command))
        #run and get the output
        try:
        	out = subprocess.check_output(command, stderr=subprocess.STDOUT)
        	
        except subprocess.TimeoutExpired:
        	print("Error timeout.")
        	continue

        for line in out.decode("utf-8").split("\n"):
            if len(line) > 0:
                if line[0] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    output_file.write(line + "\n")
        output_file.flush()

        run_output_file.write(command[3] + ',' + command[4] + ',' + "0" + ',' + "0" + ',' + "0" + '\n')
        run_output_file.flush()
        print(str(i) + "/" + str(len(commands)))

def read_models(filename):
    models = {}
    model_file = open(filename, "r")
    csv_structure = csv.reader(model_file)
    for row in csv_structure:
      color = hashStringToColor(row[1] + "".join(row[3:]))
      models[row[0]] = {"name": row[1], "file": row[2], "color": color}
      if row[1] == 'Mondrian':
          models[row[0]]["lifetime"] = row[3]
          models[row[0]]["base"] = row[4]
          models[row[0]]["discount"] = row[5]
          models[row[0]]["tree_count"] = row[6]
          models[row[0]]["memory_size"] = row[7]
          models[row[0]]["fullname"] = "Mondrian T" + row[1][row[1].find("Mondrian")+8:] + " " + row[3] + "-" + row[4] + "-" + row[5]
      elif row[1] == "MCNN":
          models[row[0]]["cluster_count"] = row[3]
          models[row[0]]["error_threshold"] = row[4]
          models[row[0]]["cleaning"] = row[5]
          models[row[0]]["perf_threshold"] = row[6]
          if row[5] == '1':
              models[row[0]]["fullname"] = "MCNN Origin " + row[3] + " (" + row[4] + ") " + row[6]
          elif row[5] == '2':
              models[row[0]]["fullname"] = "MCNN Mixe " + row[3] + " (" + row[4] + ") " + row[6]
          else:
              models[row[0]]["fullname"] = "MCNN OrpailleCC " + row[3] + " (" + row[4] + ")"
      elif row[1] == "StreamDM HoeffdingTree":
          models[row[0]]["confidence"] = row[4]
          models[row[0]]["grace_period"] = row[5]
          models[row[0]]["adaptive"] = row[3]
          if models[row[0]]["adaptive"] == "1":
              models[row[0]]["fullname"] = "StreamDM HAT c" + row[3] + " (" + row[4] + ")"
          else:
              models[row[0]]["fullname"] = "StreamDM HT c" + row[3] + " (" + row[4] + ")"
      elif row[1] == "MLP":
          models[row[0]]["learning_rate"] = row[3]
          models[row[0]]["layer_count"] = row[4]
          models[row[0]]["hidden_size"] = row[5]
          models[row[0]]["fullname"] = "MLP L" + row[3] + " (" + row[5] + ")"
      elif row[1] == "FNN":
          models[row[0]]["fullname"] = "FNN"
      else:
          models[row[0]]["fullname"] = models[row[0]]["name"]
    return models


OUTDIR="tmp_{}_{}".format(sys.argv[2], sys.argv[3])
if len(sys.argv) > 1:
    if sys.argv[1] == "compile":
        compile()
    if sys.argv[1] == "run":
        run(OUTDIR + "/output", OUTDIR + "/output_runs")
    if sys.argv[1] == "calibration":
        run(OUTDIR + "/output", OUTDIR + "/output_runs", True)
    if sys.argv[1] == "dataset":
        dataset_banos()
    if sys.argv[1] == "latex":
        latex()
