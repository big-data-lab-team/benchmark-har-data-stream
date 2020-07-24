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

def memory_list(commands):
    # for dataset_name in ['banos']:
    for dataset_name in ['drift_6', 'banos_6', 'recofit_6']:
        filename = "/tmp/" + dataset_name + ".log"
        for run_id in map(str,range(10)):
            seed = str(random.randint(0, 2**24))
            model_id = get_model_id("Empty," + filename)
            commands.append(["bin/" + dataset_name + "/empty_classifier", filename, seed, model_id, run_id])
            model_id = get_model_id("StreamDM HoeffdingTree," + filename + ",0,0.01,10")
            commands.append(["bin/" + dataset_name + "/streamdm_ht", filename, seed, model_id, run_id, "0", "0.01", "10"])
            model_id = get_model_id("NaiveBayes," + filename)
            commands.append(["bin/" + dataset_name + "/naive_bayes", filename, seed, model_id, run_id])
            model_id = get_model_id("StreamDM NaiveBayes," + filename)
            commands.append(["bin/" + dataset_name + "/streamdm_naive_bayes", filename, seed, model_id, run_id])

            model_id = get_model_id("Mondrian," + filename + ",0.8,0.1,1.0,1,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t1", filename, seed, model_id, run_id, "0.8", "0.1", "1.0"])
            model_id = get_model_id("Mondrian," + filename + ",0.8,0.0,1.0,5,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t5", filename, seed, model_id, run_id, "0.8", "0.0", "1.0"])
            model_id = get_model_id("Mondrian," + filename + ",0.6,0.0,1.0,10,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t10", filename, seed, model_id, run_id, "0.6", "0.0", "1.0"])
            model_id = get_model_id("Mondrian," + filename + ",0.6,0.0,0.1,50,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t50", filename, seed, model_id, run_id, "0.6", "0.0", "0.1"])
            model_id = get_model_id("StreamDM HoeffdingTree," + filename + ",0,0.01,10")
            commands.append(["bin/" + dataset_name + "/streamdm_ht", filename, seed, model_id, run_id, "0", "0.01", "10"])
            model_id = get_model_id("NaiveBayes," + filename)
            commands.append(["bin/" + dataset_name + "/naive_bayes", filename, seed, model_id, run_id])
            model_id = get_model_id("StreamDM NaiveBayes," + filename)
            commands.append(["bin/" + dataset_name + "/streamdm_naive_bayes", filename, seed, model_id, run_id])

            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.1,1.0,1,1200000')
            commands.append(['bin/' + dataset_name + '/mondrian_t1_double', filename, seed, model_id, run_id, '0.8', '0.1', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.0,1.0,5,1200000')
            commands.append(['bin/' + dataset_name + '/mondrian_t5_double', filename, seed, model_id, run_id, '0.8', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,1.0,10,1200000')
            commands.append(['bin/' + dataset_name + '/mondrian_t10_double', filename, seed, model_id, run_id, '0.6', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,0.1,50,1200000')
            commands.append(['bin/' + dataset_name + '/mondrian_t50_double', filename, seed, model_id, run_id, '0.6', '0.0', '0.1'])

            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.1,1.0,1,1800000')
            commands.append(['bin/' + dataset_name + '/mondrian_t1_triple', filename, seed, model_id, run_id, '0.8', '0.1', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.0,1.0,5,1800000')
            commands.append(['bin/' + dataset_name + '/mondrian_t5_triple', filename, seed, model_id, run_id, '0.8', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,1.0,10,1800000')
            commands.append(['bin/' + dataset_name + '/mondrian_t10_triple', filename, seed, model_id, run_id, '0.6', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,0.1,50,1800000')
            commands.append(['bin/' + dataset_name + '/mondrian_t50_triple', filename, seed, model_id, run_id, '0.6', '0.0', '0.1'])

            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.1,1.0,1,2400000')
            commands.append(['bin/' + dataset_name + '/mondrian_t1_quadruple', filename, seed, model_id, run_id, '0.8', '0.1', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.0,1.0,5,2400000')
            commands.append(['bin/' + dataset_name + '/mondrian_t5_quadruple', filename, seed, model_id, run_id, '0.8', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,1.0,10,2400000')
            commands.append(['bin/' + dataset_name + '/mondrian_t10_quadruple', filename, seed, model_id, run_id, '0.6', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,0.1,50,2400000')
            commands.append(['bin/' + dataset_name + '/mondrian_t50_quadruple', filename, seed, model_id, run_id, '0.6', '0.0', '0.1'])

            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.1,1.0,1,3000000')
            commands.append(['bin/' + dataset_name + '/mondrian_t1_quintuple', filename, seed, model_id, run_id, '0.8', '0.1', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.8,0.0,1.0,5,3000000')
            commands.append(['bin/' + dataset_name + '/mondrian_t5_quintuple', filename, seed, model_id, run_id, '0.8', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,1.0,10,3000000')
            commands.append(['bin/' + dataset_name + '/mondrian_t10_quintuple', filename, seed, model_id, run_id, '0.6', '0.0', '1.0'])
            model_id = get_model_id('Mondrian,' + filename + ',0.6,0.0,0.1,50,3000000')
            commands.append(['bin/' + dataset_name + '/mondrian_t50_quintuple', filename, seed, model_id, run_id, '0.6', '0.0', '0.1'])

def final_list(commands):
    # for dataset_name in ['banos']:
    for dataset_name in ["dataset_3", "dataset_2", "dataset_1", "banos_3", "recofit_3", "drift_3", "banos_6", "recofit_6", "drift_6"]:
        filename = "/tmp/" + dataset_name + ".log"
        for run_id in map(str,range(1)):
            seed = str(random.randint(0, 2**24))
            model_id = get_model_id("Empty," + filename)
            commands.append(["bin/" + dataset_name + "/empty_classifier", filename, seed, model_id, run_id])
            model_id = get_model_id("MCNN," + filename + ",10,16,0,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c10", filename, seed, model_id, run_id, "2", "0", "10"])
            model_id = get_model_id("MCNN," + filename + ",20,10,0,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c20", filename, seed, model_id, run_id, "10", "0", "10"])
            model_id = get_model_id("MCNN," + filename + ",40,8,0,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c40", filename, seed, model_id, run_id, "8", "0", "10"])
            model_id = get_model_id("MCNN," + filename + ",33,16,0,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c33", filename, seed, model_id, run_id, "16", "0", "10"])
            model_id = get_model_id("MCNN," + filename + ",50,2,0,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c50", filename, seed, model_id, run_id, "2", "0", "10"])

            model_id = get_model_id("MCNN," + filename + ",10,2,1,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c10", filename, seed, model_id, run_id, "2", "1", "10"])
            model_id = get_model_id("MCNN," + filename + ",20,10,1,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c20", filename, seed, model_id, run_id, "10", "1", "10"])
            model_id = get_model_id("MCNN," + filename + ",40,8,1,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c40", filename, seed, model_id, run_id, "8", "1", "10"])
            model_id = get_model_id("MCNN," + filename + ",33,16,1,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c33", filename, seed, model_id, run_id, "16", "1", "10"])
            model_id = get_model_id("MCNN," + filename + ",50,2,1,10")
            commands.append(["bin/" + dataset_name + "/mcnn_c50", filename, seed, model_id, run_id, "2", "1", "10"])

            model_id = get_model_id("Mondrian," + filename + ",1.0,0.1,1.0,1,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t1", filename, seed, model_id, run_id, "1.0", "0.0", "1.0"])
            model_id = get_model_id("Mondrian," + filename + ",0.4,0.0,1.0,5,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t5", filename, seed, model_id, run_id, "0.4", "0.0", "1.0"])
            model_id = get_model_id("Mondrian," + filename + ",0.4,0.0,1.0,10,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t10", filename, seed, model_id, run_id, "0.4", "0.0", "1.0"])
            model_id = get_model_id("Mondrian," + filename + ",0.2,0.0,1.0,50,600000")
            commands.append(["bin/" + dataset_name + "/mondrian_t50", filename, seed, model_id, run_id, "0.2", "0.0", "1.0"])
            model_id = get_model_id("StreamDM HoeffdingTree," + filename + ",0,0.01,10")
            commands.append(["bin/" + dataset_name + "/streamdm_ht", filename, seed, model_id, run_id, "0", "0.01", "10"])
            model_id = get_model_id("NaiveBayes," + filename)
            commands.append(["bin/" + dataset_name + "/naive_bayes", filename, seed, model_id, run_id])
            model_id = get_model_id("StreamDM NaiveBayes," + filename)
            commands.append(["bin/" + dataset_name + "/streamdm_naive_bayes", filename, seed, model_id, run_id])

            if dataset_name == 'banos_6' or dataset_name == 'recofit_6':
                model_id = get_model_id('Mondrian,' + filename + ',1.0,0.0,1.0,1,3000000')
                commands.append(['bin/' + dataset_name + '/mondrian_t1_quintuple', filename, seed, model_id, run_id, '1.0', '0.0', '1.0'])
                model_id = get_model_id('Mondrian,' + filename + ',0.4,0.0,1.0,5,3000000')
                commands.append(['bin/' + dataset_name + '/mondrian_t5_quintuple', filename, seed, model_id, run_id, '0.4', '0.0', '1.0'])
                model_id = get_model_id('Mondrian,' + filename + ',0.4,0.0,1.0,10,3000000')
                commands.append(['bin/' + dataset_name + '/mondrian_t10_quintuple', filename, seed, model_id, run_id, '0.4', '0.0', '1.0'])
                model_id = get_model_id('Mondrian,' + filename + ',0.2,0.0,1.0,50,3000000')
                commands.append(['bin/' + dataset_name + '/mondrian_t50_quintuple', filename, seed, model_id, run_id, '0.2', '0.0', '1.0'])

    for dataset_name in ["banos_3_histogram", "banos_6_histogram"]:
        filename = "/tmp/" + dataset_name + ".log"
        for run_id in map(str,range(1)):
            seed = str(random.randint(0, 2**24))
            model_id = get_model_id("FNN," + filename + ",0.1,30")
            commands.append(["bin/" + dataset_name + "/mlp_3", filename, seed, model_id, run_id, "0.1", "weights_" + dataset_name, "30"])

def run(output_filename, run_output_filename):
    output_file = open(output_filename, "w")
    run_output_file = open(run_output_filename, "w")
    commands = []
    calibration_list(commands)
    # final_list(commands)
    # memory_list(commands)

    shuffle(commands)

    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    write_model_ids("models.csv")

    #Run every commands
    for i in range(len(commands)):
        #insert energy measurement
        command = ['sudo', 'perf', 'stat', '-a', '-e', 'energy-pkg', '-e', 'energy-cores']
        command.extend(commands[i])
        print(" ".join(command))

        #run and get the output
        out = subprocess.check_output(command, stderr=subprocess.STDOUT)

        #read output line by line
        joules = 0
        seconds = 0
        for line in out.decode("utf-8").split("\n"):
            #Some lines are empty so we need to get rid of them
            if len(line) > 0:
                #If the line starts with a number, it is already a csv line
                #Otherwise, we need to check for power of timing
                if line[0] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    line = line.strip()
                    joule_index = line.find(' Joules')
                    second_index = line.find(' seconds')
                    if joule_index > 0:
                        joules += float(line[0:joule_index].replace(',', ''))
                    if second_index > 0:
                        seconds += float(line[0:second_index].replace(',', ''))
                else:
                    output_file.write(line + "\n")

        run_output_file.write(commands[i][3] + ',' + commands[i][4] + ',' + str(seconds) + ',' + str(joules) + ',' + str(joules/seconds) + '\n')

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
          # models[row[0]]["learning_rate"] = row[3]
          # models[row[0]]["layer_count"] = row[4]
          # models[row[0]]["hidden_size"] = row[5]
          models[row[0]]["fullname"] = "FNN"
      else:
          models[row[0]]["fullname"] = models[row[0]]["name"]
    return models

def process_output(output_filename, run_output_filename, model_filename):
    def add_names(row, models):
        key = str(int(row['model_id']))
        name = models[key]['name']
        if name == 'Mondrian':
            if models[key]['memory_size'] == '600000':
                return name + ' ' + models[key]['tree_count'] + ' tree(s)'
            else:
                return name + ' ' + models[key]['tree_count'] + ' tree(s) (RAM x' + str(int(models[key]['memory_size']) / 600000) + ')'
        elif name == 'MCNN':
            if models[key]['cleaning'] == '1':
                return 'MCNN Origin ' + models[key]['cluster_count'] + ' clusters'
            elif models[key]['cleaning'] == '2':
                return 'MCNN Mixe ' + models[key]['cluster_count'] + ' clusters'
            else:
                return 'MCNN OrpailleCC ' + models[key]['cluster_count'] + ' clusters'
        elif name == 'StreamDM HoeffdingTree':
            return name
        else:
            return models[key]['fullname']
    def add_files(row, models):
        return models[str(int(row['model_id']))]['file']
    def add_color(row, models):
        return models[str(int(row['model_id']))]['color']
    def add_library(row, models):
        if models[str(int(row['model_id']))]['fullname'].find('StreamDM') >= 0:
            return 'StreamDM'
        return 'OrpailleCC'
    def add_algorithm(row, models):
        if models[str(int(row['model_id']))]['fullname'].find('Naive') >= 0:
            return 'NaiveBaye'
        if models[str(int(row['model_id']))]['fullname'].find('Naive') >= 0:
            return 'NaiveBaye'
        if models[str(int(row['model_id']))]['fullname'].find('Mondrian') >= 0:
            return 'Mondrian Forest'
        if models[str(int(row['model_id']))]['fullname'].find('MCNN') >= 0:
            return 'MCNN'
        if models[str(int(row['model_id']))]['fullname'].find('MLP') >= 0:
            return 'MLP'
        if models[str(int(row['model_id']))]['fullname'].find('FNN') >= 0:
            return 'FNN'
        return 'Unknown'

    models = read_models(model_filename)
    output = pd.read_csv(output_filename)
    output_runs = pd.read_csv(run_output_filename)
    output.columns = ['model_id', 'run_id', 'element_count', 'seed', 'accuracy', 'f1', 'memory']
    output_runs.columns = ['model_id', 'run_id', 'time', 'energy', 'power']
    print("Adding Fullname")
    output['fullname'] = output.apply(lambda r: add_names(r, models), axis=1)
    print("Adding File")
    output['file'] = output.apply(lambda r: add_files(r, models), axis=1)

    print("Adding to output run")
    output_runs['fullname'] = output_runs.apply(lambda r: add_names(r, models), axis=1)
    output_runs['file'] = output_runs.apply(lambda r: add_files(r, models), axis=1)
    output_runs['color'] = output_runs.apply(lambda r: add_color(r, models), axis=1)
    output_runs['library'] = output_runs.apply(lambda r: add_library(r, models), axis=1)
    output_runs['algorithm'] = output_runs.apply(lambda r: add_algorithm(r, models), axis=1)
    return (output, output_runs, models)

def print_results(output, output_runs, models, output_directory="."):
    def add_markers(x):
        if x[0].find('FNN') >= 0:
            return 's'
        elif x[0].find('MCNN') >= 0:
            if models[x[1]]['cluster_count'] == '10':
                return 's'
            if models[x[1]]['cluster_count'] == '20':
                return 'o'
            if models[x[1]]['cluster_count'] == '33':
                return '*'
            if models[x[1]]['cluster_count'] == '40':
                return 'x'
            if models[x[1]]['cluster_count'] == '50':
                return '^'
        elif x[0].find('Mondrian') >= 0:
            if models[x[1]]['tree_count'] == '10':
                return '*'
            elif models[x[1]]['tree_count'] == '50':
                return 'x'
            elif models[x[1]]['tree_count'] == '1':
                return 's'
            elif models[x[1]]['tree_count'] == '5':
                return 'o'
        elif x[0].find('NaiveBayes') >= 0:
            return 's'
        elif x[0].find('HT') >= 0 or x[0].find('Hoeffding') >= 0:
            return 's'
        elif x[0].find('Empty') >= 0:
            return 's'
        return ''
    def add_colors(x):
        if x[0].find('FNN') >= 0:
            return '#9400D3'
        elif x[0].find('MCNN') >= 0:
            if models[x[1]]['cleaning'] == '0':
                return '#5BE33D'
            else:
                return '#FF69B4'
        elif x[0].find('Mondrian') >= 0:
            if models[x[1]]['memory_size'] == '600000':
                return '#00BFFF'
            if models[x[1]]['memory_size'] == '1200000':
                return '##9400D3'
            if models[x[1]]['memory_size'] == '1800000':
                return '#FF69B4'
            if models[x[1]]['memory_size'] == '2400000':
                return '#5BE33D'
            if models[x[1]]['memory_size'] == '3000000':
                return '#0048FF'
        elif x[0].find('NaiveBayes') >= 0:
            return '#F20B13'
        elif x[0].find('HT') >= 0 or x[0].find('HoeffdingTree') >= 0:
            return '#FF8A00'
        elif x[0].find('Empty') >= 0:
            return '#000000'
        elif x[0].find('Previous') >= 0:
            return '#FFB6C1'
        return ''
    def add_style(x):
        if x[0].find('StreamDM') >= 0:
            return ':'
        return '-'
    def add_key(key):
        name = models[key]['name']
        if name == 'Mondrian':
            if models[key]['memory_size'] == '600000':
                return (name + ' ' + models[key]['tree_count'] + ' tree(s)', key, (name, int(models[key]['tree_count'])))
            else:
                ram_count = str(int(models[key]['memory_size']) / 600000)
                return (name + ' ' + models[key]['tree_count'] + ' tree(s) (RAM x' + ram_count + ')', key, (name + ' (RAM x' + ram_count + ')', int(models[key]['tree_count'])))
        elif name == 'MCNN':
            if models[key]['cleaning'] == '1':
                return ('MCNN Origin ' + models[key]['cluster_count'] + ' clusters', key, ('MCNN Origin', int(models[key]['cluster_count'])))
            elif models[key]['cleaning'] == '2':
                return ('MCNN Mixe ' + models[key]['cluster_count'] + ' clusters', key, ('MCNN Mixe', int(models[key]['cluster_count'])))
            else:
                return ('MCNN OrpailleCC ' + models[key]['cluster_count'] + ' clusters', key, ('MCNN OrpailleCC', int(models[key]['cluster_count'])))
        else:
            return (name, key, (name, 0))

    dataset_title = {'banos_3': 'Banos et al', 'recofit_3': 'Recofit', 'drift_3': 'Banos et al (Drift)', 'dataset_1': 'Hyperplane', 'dataset_2' : 'RandomRBF', 'dataset_3' : 'RandomTree', 'banos_6': 'Banos et al, 6 axis', 'recofit_6': 'Recofit 6 axis', 'drift_6' : 'Banos et al 6 axis (Drift)'}
    #(print name, key in models, tuple for sorting)
    keys = [add_key(key) for key in models if models[key]['fullname'] != 'Previous']
    #grounp the third and second value to use dict to do a unique
    keys = dict([(key[0], (key[1], key[2])) for key in keys]).items()
    #Unpack the value part to separate the key and the sorting tuple
    keys = [(key[0], key[1][0], key[1][1]) for key in keys]
    keys = sorted(keys, key = lambda x: x[2])
    names = [key[0] for key in keys]
    colors = [add_colors(key) for key in keys]
    markers = [add_markers(key) for key in keys]
    styles = [add_style(key) for key in keys]
    knn_offline_f1 = {'banos_3': 0.0, 'recofit_3': 0.0, 'drift_3': 0.0, 'dataset_1': 0.95, 'dataset_2' : 0.78, 'dataset_3' : 0.69, 'banos_6': 0.86, 'recofit_6': 0.40, 'drift_6' : 0.86}
    print(names)
    print(colors)
    print(markers)
    print(styles)
    plt.rcParams.update({'font.size': 27})
    list_datastets = ['dataset_2', 'drift_3', 'banos_3', 'recofit_3', 'dataset_1', 'dataset_2', 'dataset_3', 'drift_6', 'banos_6', 'recofit_6']
    for dataset_name in list_datastets:
        print('Dataset: ' + dataset_name)
        print('\t- Energy')
        fig = plt.figure(figsize=(23.38582, 16.53544))
        ax = sns.boxplot(x="fullname", hue="fullname", y="energy", data=output_runs[output_runs.file.str.contains(dataset_name)], order=names, palette=colors, hue_order=names, dodge=False, boxprops=dict(alpha=.3))
        ax.legend().remove()
        ax = sns.swarmplot(x="fullname", y="energy", data=output_runs[output_runs.file.str.contains(dataset_name)], order=names, palette=colors, hue_order=names, alpha=0.75)
        ax.legend().remove()
        plt.xticks(rotation=90)
        plt.ylabel("Joules")
        plt.xlabel("Algorithm")
        plt.tight_layout()
        plt.savefig(output_directory + "/" + dataset_name + "_energy" + ".png")
        plt.clf()

        print('\t- Power')
        fig = plt.figure(figsize=(23.38582, 16.53544))
        ax = sns.boxplot(x="fullname", hue="fullname", y="power", data=output_runs[output_runs.file.str.contains(dataset_name)], palette=colors, order=names, hue_order=names, dodge=False, boxprops=dict(alpha=.3))
        ax.legend().remove()
        ax = sns.swarmplot(x="fullname", y="power", data=output_runs[output_runs.file.str.contains(dataset_name)], order=names, palette=colors, hue_order=names, alpha=0.75)
        ax.legend().remove()
        plt.ylim(95, 105)
        plt.xticks(rotation=90)
        plt.ylabel("Watt")
        plt.xlabel("Algorithm")
        plt.tight_layout()
        plt.savefig(output_directory + "/" + dataset_name + "_watt" + ".png")
        plt.clf()

        print('\t- Time')
        fig = plt.figure(figsize=(23.38582, 16.53544))
        ax = sns.boxplot(x="fullname", hue="fullname", y="time", data=output_runs[output_runs.file.str.contains(dataset_name)], order=names, palette=colors, hue_order=names, dodge=False, boxprops=dict(alpha=.3))
        ax.legend().remove()
        ax = sns.swarmplot(x="fullname", y="time", data=output_runs[output_runs.file.str.contains(dataset_name)], order=names, palette=colors, hue_order=names, alpha=0.75)
        ax.legend().remove()
        plt.xticks(rotation=90)
        plt.ylabel("Dataset processing time (seconds)")
        plt.xlabel("Algorithm")
        plt.tight_layout()
        plt.savefig(output_directory + "/" + dataset_name + "_runtime" + ".png")
        plt.clf()

        daty = output[output.file.str.contains(dataset_name)]
        daty_std = daty[['fullname', 'element_count', 'f1', 'accuracy', 'memory']].groupby(['fullname', 'element_count']).std().reset_index()
        daty = daty[['fullname', 'element_count', 'f1', 'accuracy', 'memory']].groupby(['fullname', 'element_count']).mean().reset_index()


        print('\t- F1')
        fig = plt.figure(figsize=(23.38582, 16.53544))

        for name, color, marker, style in zip(names, colors, markers, styles):
            plt.plot(daty[daty.fullname == name]['element_count'], daty[daty.fullname == name]['f1'], color=color, marker=marker, linestyle=style, markevery=0.1, markersize=15, label=name)
        # if dataset_name == 'banos_3' or dataset_name == 'banos_6':
            # plt.legend(prop={"size":27}, ncol=3)
        if dataset_name in knn_offline_f1:
            x = [a for a in daty[daty.fullname == name]['element_count']]
            y = [knn_offline_f1[dataset_name] for a in daty[daty.fullname == name]['element_count']]
            plt.plot(x, y, color='#000000', linestyle='-.', label='KNN Offline')

        plt.ylim(0,1)
        plt.ylabel("F1")
        plt.xlabel("Element")
        plt.tight_layout()
        plt.savefig(output_directory + "/" + dataset_name + "_f1" + ".png")
        plt.clf()

        # if dataset_name == 'banos_3' or dataset_name == 'banos_6':
            # print('\t- legend')
            # # fig = plt.figure(figsize=(23.38582, 16.53544))

            # zeross = [0 for i in daty[daty.fullname == name]['element_count']]
            # x = [i for i in daty[daty.fullname == name]['element_count']]
            # print(len(zeross))
            # print(daty[daty.fullname == name]['element_count'])
            # for name, color, marker, style in zip(names, colors, markers, styles):
                # plt.plot(x, zeross, color=color, marker=marker, linestyle=style, markevery=0.1, markersize=15, label=name)

            # plt.legend(prop={"size":23}, ncol=3)
            # plt.ylim(0,1)
            # plt.tight_layout()
            # plt.show()
            # plt.savefig(output_directory + "/" + dataset_name + "_legend.png")
            # plt.clf()

        print('\t- F1 stdv')
        fig = plt.figure(figsize=(23.38582, 16.53544))
        for name, color, marker, style in zip(names, colors, markers, styles):
            y1 = daty[daty.fullname == name]['f1'] - daty_std[daty_std.fullname == name]['f1']
            y2 = daty[daty.fullname == name]['f1'] + daty_std[daty_std.fullname == name]['f1']
            plt.plot(daty[daty.fullname == name]['element_count'], daty[daty.fullname == name]['f1'], color=color, marker=marker, linestyle=style, markevery=0.1, markersize=15, label=name)
            plt.fill_between(daty_std[daty_std.fullname == name]['element_count'], y1, y2, color=color, linestyle=style, alpha=0.2)
        if dataset_name in knn_offline_f1:
            x = [a for a in daty[daty.fullname == name]['element_count']]
            y = [knn_offline_f1[dataset_name] for a in daty[daty.fullname == name]['element_count']]
            plt.plot(x, y, color='#000000', linestyle='-.', label='KNN Offline')
        # if dataset_name == 'banos_3' or dataset_name == 'banos_6':
            # plt.legend(prop={"size":25}, ncol=3)
        plt.ylim(0,1)
        plt.ylabel("F1")
        plt.xlabel("Element")
        plt.tight_layout()
        plt.savefig(output_directory + "/" + dataset_name + "_f1_std" + ".png")
        plt.clf()


        print('\t- Accuracy')
        fig = plt.figure(figsize=(23.38582, 16.53544))
        for name, color, marker, style in zip(names, colors, markers, styles):
            plt.plot(daty[daty.fullname == name]['element_count'], daty[daty.fullname == name]['accuracy'], color=color, marker=marker, linestyle=style, markevery=0.1, markersize=15, label=name)
        if dataset_name == 'banos_3' or dataset_name == 'banos_6':
            plt.legend(prop={"size":25}, ncol=3)
        plt.ylim(0,1)
        plt.ylabel("Accuracy")
        plt.xlabel("Element")
        plt.tight_layout()
        plt.savefig(output_directory + "/" + dataset_name + "_accuracy" + ".png")
        plt.clf()

        print('\t- Memory ' + str(daty[daty.fullname == 'Empty']['memory'][0]))
        fig = plt.figure(figsize=(23.38582, 16.53544))
        for name, color, marker, style in zip(names, colors, markers, styles):

            if 'StreamDM' in name:
                base = [x for x in daty[daty.fullname == 'StreamDM NaiveBayes']['memory']]
            else:
                base = [x for x in daty[daty.fullname == 'NaiveBayes']['memory']]
            if len(daty[daty.fullname == name]['memory']) == len(daty[daty.fullname == 'Empty']['memory']):
                y = [x[0] - x[1] for x in zip(daty[daty.fullname == name]['memory'], base)]
                plt.plot(daty[daty.fullname == name]['element_count'], y, color=color, marker=marker, linestyle=style, markevery=0.1, markersize=15, label=name)
        if dataset_name == 'banos_3' or dataset_name == 'banos_6':
            plt.legend(prop={"size":26}, ncol=3)
        plt.ylabel("KB")
        plt.xlabel("Element")
        plt.tight_layout()
        plt.savefig(output_directory + "/" + dataset_name + "_memory" + ".png")
        plt.clf()

def print_calibration(output, output_runs, models, output_directory="."):
    def mondrian_lifetime(key, tree_count):
        name = models[key]['name']
        if name == 'Mondrian' and models[key]['tree_count'] == tree_count and models[key]['discount'] == '0.2' and models[key]['base'] == '0.1':
            return True
        return False
    def mondrian_discount(key, tree_count):
        name = models[key]['name']
        if name == 'Mondrian' and models[key]['tree_count'] == tree_count and models[key]['lifetime'] == '1.0' and models[key]['base'] == '0.1':
            return True
        return False
    def mondrian_base(key, tree_count):
        name = models[key]['name']
        if name == 'Mondrian' and models[key]['tree_count'] == tree_count and models[key]['lifetime'] == '1.0' and models[key]['discount'] == '0.2':
            return True
        return False
    def mcnn_error(key, cluster_count, cleaning):
        name = models[key]['name']
        if name == 'MCNN' and models[key]['cluster_count'] == cluster_count and models[key]['cleaning'] == cleaning:
            return True
        return False
    def mondrian_by_tree(key, tree_count):
        name = models[key]['name']
        if name == 'Mondrian' and models[key]['tree_count'] == tree_count:
            return True
        return False

    plt.rcParams.update({'font.size': 26})
    dataset_name = "processed_subject1_ideal_shuf.log"

    daty = output[output.file.str.contains(dataset_name)]
    daty = daty[['model_id', 'element_count', 'f1', 'accuracy', 'memory']].groupby(['model_id', 'element_count']).mean().reset_index()
    keys = [key for key in models if mondrian_lifetime(key, '10') == True]
    m = daty['model_id'].isin(keys)
    daty = daty[m]
    model_ids = daty.model_id.unique()
    fig = plt.figure(figsize=(23.38582, 16.53544))
    for model_id in model_ids:
        sub = daty[daty.model_id == model_id]
        plt.plot(sub['element_count'], sub['f1'], color=hashStringToColor(str(model_id)), label='Mondrian ' + models[str(model_id)]['lifetime'])
    plt.legend(prop={"size":25}, ncol=3)
    plt.ylim(0,1)
    plt.ylabel("F1")
    plt.xlabel("Element")
    plt.tight_layout()
    plt.savefig(output_directory + "/calibration_mondrian_lifetime.png")
    plt.clf()

    daty = output[output.file.str.contains(dataset_name)]
    daty = daty[['model_id', 'element_count', 'f1', 'accuracy', 'memory']].groupby(['model_id', 'element_count']).mean().reset_index()
    keys = [key for key in models if mondrian_discount(key, '10') == True]
    m = daty['model_id'].isin(keys)
    daty = daty[m]
    model_ids = daty.model_id.unique()
    fig = plt.figure(figsize=(23.38582, 16.53544))
    for model_id in model_ids:
        sub = daty[daty.model_id == model_id]
        plt.plot(sub['element_count'], sub['f1'], color=hashStringToColor(str(model_id)), label='Mondrian ' + models[str(model_id)]['discount'])
    plt.legend(prop={"size":25}, ncol=3)
    plt.ylim(0,1)
    plt.ylabel("F1")
    plt.xlabel("Element")
    plt.tight_layout()
    plt.savefig(output_directory + "/calibration_mondrian_discount.png")
    plt.clf()

    daty = output[output.file.str.contains(dataset_name)]
    daty = daty[['model_id', 'element_count', 'f1', 'accuracy', 'memory']].groupby(['model_id', 'element_count']).mean().reset_index()
    keys = [key for key in models if mondrian_base(key, '10') == True]
    m = daty['model_id'].isin(keys)
    daty = daty[m]
    model_ids = daty.model_id.unique()
    fig = plt.figure(figsize=(23.38582, 16.53544))
    for model_id in model_ids:
        sub = daty[daty.model_id == model_id]
        plt.plot(sub['element_count'], sub['f1'], color=hashStringToColor(str(model_id)), label='Mondrian ' + models[str(model_id)]['base'])
    plt.legend(prop={"size":25}, ncol=3)
    plt.ylim(0,1)
    plt.ylabel("F1")
    plt.xlabel("Element")
    plt.tight_layout()
    plt.savefig(output_directory + "/calibration_mondrian_base.png")
    plt.clf()

    for cluster_count in ['10', '20', '40']:
        daty = output[output.file.str.contains(dataset_name)]
        daty = daty[['model_id', 'element_count', 'f1', 'accuracy', 'memory']].groupby(['model_id', 'element_count']).mean().reset_index()
        keys = [key for key in models if mcnn_error(key, cluster_count, '0') == True]
        m = daty['model_id'].isin(keys)
        daty = daty[m]
        model_ids = daty.model_id.unique()
        fig = plt.figure(figsize=(23.38582, 16.53544))
        for model_id in model_ids:
            sub = daty[daty.model_id == model_id]
            plt.plot(sub['element_count'], sub['f1'], color=hashStringToColor(str(model_id)), label='MCNN ' + models[str(model_id)]['error_threshold'])
        plt.legend(prop={"size":25}, ncol=3)
        plt.ylim(0,1)
        plt.ylabel("F1")
        plt.xlabel("Element")
        plt.tight_layout()
        plt.savefig(output_directory + "/calibration_mcnn_" + cluster_count + ".png")
        plt.clf()

    print("look best of")
    daty = output[output.file.str.contains(dataset_name)]
    daty = daty[['model_id', 'element_count', 'f1', 'accuracy', 'memory']].groupby(['model_id', 'element_count']).mean().reset_index()
    for cluster_count in ['10', '20', '33', '40', '50']:
        keys = [key for key in models if mcnn_error(key, cluster_count, '0') == True]
        average = 0
        best_model = '-1'
        for model_id in keys:
            sub = mean(daty[daty.model_id == int(model_id)]['f1'][-250:])
            if sub > average:
                average = sub
                best_model = str(model_id)
        print('MCNN ' + cluster_count + ': ' + str(models[best_model]))
    for tree_count in ['1', '5', '10', '50']:
        keys = [key for key in models if mondrian_by_tree(key, tree_count) == True]
        average = 0
        best_model = -1
        for model_id in keys:
            sub = mean(daty[daty.model_id == int(model_id)]['f1'][-250:])
            if sub > average:
                average = sub
                best_model = str(model_id)
        print('Mondrian ' + tree_count + ': ' + str(models[best_model]))

def additional_computation(results):
    print("Done")
    filename = "processed_subject1_ideal_shuf.log"
    pattern = re.compile("Mondrian T10 1.0-.*")
    # filename = "dataset_1.arff"
    # for pattern in [re.compile("Mondrian T10 0.8-0.0.*"), \
            # re.compile("MLP.*"), \
            # re.compile("Mondrian T10 1.0-.*"), \
            # re.compile("Mondrian T1 1.0-.*"), \
            # re.compile("Mondrian T1(0)? 1.0-[0\\.1]{3}-.*"), \
            # re.compile("Mondrian T[0-9]+ 1.0-0.5-.*"), \
            # re.compile("Mondrian T[0-9]+ 1.0-0.1-.*"), \
            # re.compile("Mondrian T1 .{3}-0.5-.*"), \
            # re.compile("Mondrian T1 .{3}-0.1-.*"), \
            # re.compile("Mondrian T10 .{3}-0.1-.*"), \
            # # re.compile("(HT.*|HAT.*)"), \
            # # re.compile("(HT.*|HAT.*)"), \
            # re.compile("MCNN 40.*"),\
            # re.compile("MCNN 10.*"),\
            # re.compile("MCNN 20.*")
            # ]:
        # break
        # for model in results:
            # if pattern.match(model):
                # tmp = results[model][filename]["accuracy"]
                # x = [d[0] for d in tmp]
                # plt.plot(x, [d[1] for d in tmp], label=model, color=results[model][filename]["color"])

        # # plt.plot([x/33 for x in class_repartition], label="Hipster")
        # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        # plt.savefig("perf_accuracy.png", bbox_inches="tight")
        # plt.ylabel("Accuracy")
        # plt.xlabel("Element")
        # plt.ylim(0,1)
        # plt.show()
        # plt.clf()

    print("look best of")
    for pattern in [\
                    re.compile("MCNN 50 [^C]*C0.*"), \
                    re.compile("MCNN 50 [^C]*C1.*"), \
                    re.compile("MCNN 50 [^C]*C1 - 50.*"), \
                    re.compile("Hoeffding"), \
                    re.compile("Empty")]:
        model_name = []
        average = 0
        for model in results:
            if pattern.match(model):
                m = mean([d[1] for d in results[model][filename]["accuracy"][-250:]])
                if m > average:
                    actual_plot = model
                    average = m
        tmp = results[actual_plot][filename]["accuracy"]
        x = [d[0] for d in tmp]
        plt.plot(x, [d[1] for d in tmp], label=actual_plot, color=results[actual_plot][filename]["color"])

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("perf_accuracy.png", bbox_inches="tight")
    plt.ylabel("Accuracy")
    plt.xlabel("Element")
    plt.ylim(0,1)
    plt.show()
    plt.clf()

    for model in results:
        tmp = results[model][filename]["f1"]
        x = [d[0] for d in tmp]
        plt.plot(x, [d[1] for d in tmp], label=model, color=results[model][filename]["color"])

    # plt.plot([x/33 for x in class_repartition], label="Hipster")
    plt.ylabel("F1-score")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("perf_f1.png", bbox_inches="tight")
    plt.clf()

    for model in results:
        tmp = results[model][filename]["memory"]
        x = [d[0] for d in tmp]
        plt.plot(x, [d[1] for d in tmp], label=model)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("memory.png", bbox_inches="tight")
    plt.clf()

    heights = [mean(map(float, results[model][filename]["energy"])) for model in results]
    x = [model for model in results]
    plt.bar([i for i in range(len(x))], heights)
    plt.xticks([i for i in range(len(x))], x, rotation=90)

    plt.ylabel("Joules")
    plt.rcParams["figure.figsize"][0] = 10
    plt.rcParams["figure.figsize"][1] = 10
    plt.savefig("runs_energy.png", bbox_inches="tight")

    plt.clf()

    heights = [mean(map(float, results[model][filename]["time"])) for model in results]
    x = [model for model in results]
    plt.bar([i for i in range(len(x))], heights)
    plt.xticks([i for i in range(len(x))], x, rotation=90)

    plt.ylabel("Seconds")
    plt.savefig("runs_time.png", bbox_inches="tight")

    plt.clf()

def aggregate_list_measurement(measurements):
    #measurements = [[d1, d2, d3], [d4, d5, d6]]
    #d1 = [x, y]
    #d1 and d4 may share the same x

    x_save = {}
    for measurement in measurements:
        for data in measurement:
            x = float(data[0])
            y = float(data[1])
            if x in x_save:
                x_save[x].append(y)
            else:
                x_save[x] = [y]
    keys = list(x_save.keys())
    keys.sort()
    tmp = [[x, mean(x_save[x]), stdev(x_save[x]), min(x_save[x]), max(x_save[x])] for x in keys]
    return tmp


if len(sys.argv) > 1:
    if sys.argv[1] == "compile":
        compile()
    if sys.argv[1] == "run":
        run("/tmp/output", "/tmp/output_runs")
    if sys.argv[1] == "dataset":
        dataset_banos()
    if sys.argv[1] == "latex":
        latex()
    if sys.argv[1] == "process":
        # results = process_output("calibration/output", "calibration/output_runs", "calibration/models.csv")
        directory = "results_9/"
        output, output_runs, models = process_output(directory + "output", directory + "output_runs", directory + "models.csv")
        # print_results(output[output.element_count%50 == 0],  output_runs, models)
        print_results(output, output_runs, models)
        # print_calibration(output, output_runs, models)

