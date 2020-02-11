import subprocess
import sys
import math
import os
import csv
import random
import statistics
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
def dataset():
    output_directory = "/tmp/"
    input_directory = "sensor_dataset/"
    filenames = ["subject1_ideal.log"]
    # filenames = ["subject" + str(i) + "_ideal.log" for i in range(1, 18)]
    for filename in filenames:
        try:
            in_f = open(input_directory + filename,"r")
            output_filename = output_directory + \
                                "processed_" + \
                                os.path.basename(filename)
            out_f = open(output_filename,"w")
            process_file(in_f, out_f, 50)
            print(filename)
        except IOError:
            print("Could not open file: " + filename)
    return

def process_file(in_f, out_f, window_size):
    window = []
    for line in in_f:
        window.append(line.split("\t"))
        if len(window) >= window_size:
            features = extract_features(window)
            window = []
            out_f.write("\t".join(features) + "\n")

def extract_features(window):
    starting_index = 2
    window_transposed = [[float(i) for i in x] for x in zip(*window)]

    features = []
    for i in range(2, 5):
        features.append(mean(window_transposed[i]))
        features.append(stdev(window_transposed[i]))
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

def run(output_filename, run_output_filename):
    dataset_filenames = ["/tmp/processed_subject1_ideal_shuf.log"]
    # dataset_filenames = ["sensor_dataset/windowed/processed_full_shuf.log"]
    # dataset_filenames = ["dataset_1.arff"]
    output_file = open(output_filename, "w")
    run_output_file = open(run_output_filename, "w")
    commands = []
    for filename in dataset_filenames:
        for run_id in map(str,range(1)):
            seed = str(random.randint(0, 2**24))
            model_id = get_model_id("Empty," + filename)
            commands.append(["./empty_classifier", filename, seed, model_id, run_id])
            model_id = get_model_id("Previous," + filename)
            commands.append(["./previous_classifier", filename, seed, model_id, run_id])

            for cluster in ["10", "20", "31", "33", "34", "40", "50", "100"]:
                model_id = get_model_id("MCNN," + filename + "," + cluster + ",10,10")
                commands.append(["./mcnn_c" + cluster + "e10p10", filename, seed, model_id, run_id])

            model_id = get_model_id("HoeffdingTree," + filename)
            commands.append(["./streamdm", filename, seed, model_id, run_id])

            # for base_count in ["0.1", "0.2", "0.3", "0.4", "0.5", "1.0", "1.2", "1.4", "1.6"]:
                # for budget in ["2.0", "1.8", "1.6", "1.4", "1.2", "1.0", "0.8", "0.6"]:
                    # for tree_count in [1, 5, 10, 50]:
                        # model_id = get_model_id("Mondrian" + str(tree_count) + "," + filename + "," + budget + "," + base_count + "," + "0.2")
                        # commands.append(["./mondrian_t" + str(tree_count), filename, seed, model_id, run_id, budget, base_count, "0.2"])


    shuffle(commands)

    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    write_model_ids("models.csv")

    #Run every commands
    for i in range(len(commands)):
        command = commands[i]
        #insert energy measurement
        command.insert(0,"./AppPowerMeter")
        print(" ".join(command))

        #run and get the output
        out = subprocess.check_output(command)

        #read output line by line
        for line in out.decode("utf-8").split("\n"):
            #Some lines are empty so we need to get rid of them
            if len(line) > 0:
                #If the line starts with a number, it is already a csv line
                #Otherwise, we need to check for power of timing
                if line[0] not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    if line.startswith("\tTotal Energy:\t"):
                        joule_index = line.find(" J", 15)
                        energy = line[15:joule_index]
                        run_output_file.write(command[4] + "," + command[5] + ",," + energy + "\n")
                        #The line of power contains the linecount of -1
                    if line.startswith("\tTime:\t"):
                        sec_index = line.find(" sec", 7)
                        timy = line[7:sec_index]
                        run_output_file.write(command[4] + "," + command[5] + "," + timy + ",\n")
                        #The line of power contains the linecount of -1
                else:
                    output_file.write(line + "\n")

        print(str(i) + "/" + str(len(commands)))

def process_output(output_filename, run_output_filename, model_filename):
    models = {}
    model_file = open(model_filename, "r")
    csv_structure = csv.reader(model_file)
    #Read the model file
    for row in csv_structure:
        color = hashStringToColor(row[1] + "".join(row[3:]))
        models[row[0]] = {"name": row[1], "file": row[2], "color": color}
        if row[1] == "Mondrian":
            models[row[0]]["lifetime"] = row[3]
            models[row[0]]["base"] = row[4]
            models[row[0]]["discount"] = row[5]
            models[row[0]]["fullname"] = "Mondrian " + row[3] + "-" + row[4] + "-" + row[5]
        elif row[1] == "MCNN":
            models[row[0]]["cluster_count"] = row[3]
            models[row[0]]["error_threshold"] = row[4]
            models[row[0]]["p"] = row[5]
            models[row[0]]["fullname"] = "MCNN " + row[3] + " (" + row[4] + ")"
        else:
            models[row[0]]["fullname"] = models[row[0]]["name"]


    results = {}

    #Read the output file that contains output about the data processed.
    output_file = open(output_filename, "r")
    csv_structure = csv.reader(output_file)
    for row in csv_structure:
        name = models[row[0]]["fullname"]
        filename = models[row[0]]["file"]
        color = models[row[0]]["color"]
        if name not in results:
            results[name] = {filename : {"color": color, "accuracy": {}, "energy": [], "time": [], "f1": {}, "memory": {}}}
        elif filename not in results[name]:
            results[name][filename] = {"color": color, "accuracy": {}, "energy": [], "time": [], "f1": {}, "memory": {}}

        #I know, it is awful :) Enjoy reading this code
        for type_perf in [("accuracy", 5), ("f1", 4), ("memory", 6)]:
            perf_name = type_perf[0]
            perf_idx = type_perf[1]
            if len(row[perf_idx]) > 0:
                if row[1] not in results[name][filename][perf_name]:
                    results[name][filename][perf_name][row[1]] = [[row[2], row[perf_idx]]]
                else:
                    results[name][filename][perf_name][row[1]].append([row[2], row[perf_idx]])

    #Read the run output file that contains data about the run itself.
    run_output_file = open(run_output_filename, "r")
    csv_structure = csv.reader(run_output_file)
    for row in csv_structure:
        name = models[row[0]]["fullname"]
        filename = models[row[0]]["file"]
        #The name should exist, otherwise that would mean there wasn't any other output for this (model,filename)
        if row[3] != "":
            results[name][filename]["energy"].append(float(row[3]))
        if row[2] != "":
            results[name][filename]["time"].append(float(row[2]))

    for model_name in results:
        for filename in results[model_name]:
            results[model_name][filename]["accuracy"] = [ results[model_name][filename]["accuracy"][key] for key in results[model_name][filename]["accuracy"]]
            results[model_name][filename]["f1"] = [ results[model_name][filename]["f1"][key] for key in results[model_name][filename]["f1"]]
            results[model_name][filename]["memory"] = [ results[model_name][filename]["memory"][key] for key in results[model_name][filename]["memory"]]

    # results = {} #{model name: {filename: {accuracy: [AA], energy: [value for each run]}}}
                 #[AA]: a list of accuracy for each run
                 # AA : a list of accuracy, each element contains [number of data points, accuracy]

    return results

def additional_computation(results):
    for model in results:
        for filename in results[model]:
            results[model][filename]["f1"] = aggregate_list_measurement(results[model][filename]["f1"])
            results[model][filename]["accuracy"] = aggregate_list_measurement(results[model][filename]["accuracy"])
            results[model][filename]["memory"] = aggregate_list_measurement(results[model][filename]["memory"])

    filename = "/tmp/processed_subject1_ideal_shuf.log"
    # filename = "dataset_1.arff"
    # model_name = "Mondrian Lifetime: 2 Base measure: 0.5 Discount factor: 0.2 Tree count: 10"
    for model in results:
        tmp = results[model][filename]["accuracy"]
        x = [d[0] for d in tmp]
        plt.plot(x, [d[1] for d in tmp], label=model, color=results[model][filename]["color"])

    # plt.plot([x/33 for x in class_repartition], label="Hipster")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("perf_accuracy.png", bbox_inches="tight")
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

    plt.show()
    plt.clf()

    heights = [mean(map(float, results[model][filename]["time"])) for model in results]
    x = [model for model in results]
    plt.bar([i for i in range(len(x))], heights)
    plt.xticks([i for i in range(len(x))], x, rotation=90)

    plt.ylabel("Seconds")
    plt.rcParams["figure.figsize"][0] = 10
    plt.rcParams["figure.figsize"][1] = 10
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
        dataset()
    if sys.argv[1] == "latex":
        latex()
    if sys.argv[1] == "process":
        results = process_output("/tmp/output", "/tmp/output_runs", "models.csv")
        additional_computation(results)

