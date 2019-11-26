import subprocess
import sys
import math
import os
import statistics
from statistics import mean
import matplotlib.pyplot as plt
from random import shuffle

def stdev(l):
    if len(l) <= 1:
        return 0.0
    return statistics.stdev(l)

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
    filenames = ["subject1_ideal.log", "subject2_ideal.log"]
    for filename in filenames:
        try:
            in_f = open(input_directory + filename,"r")
            output_filename = output_directory + \
                                "processed_" + \
                                os.path.basename(filename)
            out_f = open(output_filename,"w")
            process_file(in_f, out_f, 50)
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

def run(output_filename):
    dataset_filenames = ["/tmp/processed_subject1_ideal.log"]
    output_file = open(output_filename, "w")
    commands = []
    for filename in dataset_filenames:
        for i in range(10):
            commands.append(["./empty_classifier", filename])
            commands.append(["./mcnn_c20e10p10", filename])
            for lt in ["2.0", "1.8", "0.8", "0.6"]:
                commands.append(["./mondrian_t10", filename, lt, "0.5", "0.2"])

    shuffle(commands)

    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    for i in range(len(commands)):
        command = commands[i]
        command.insert(0,"./AppPowerMeter")
        # if i > 0:
            # print(CURSOR_UP_ONE + CURSOR_UP_ONE + ERASE_LINE)
        print(" ".join(command))
        subprocess.call(command, stdout=output_file)
        # if i > 0:
            # print(ERASE_LINE)
        print(str(i) + "/" + str(len(commands)))

def process_output(filename):
    input_file = open(filename,"r")
    results = {} #{model name: {filename: {accuracy: [AA], energy: [value for each run]}}}
                 #[AA]: a list of accuracy for each run
                 # AA : a list of accuracy, each element contains [number of data points, accuracy]
    current_model = ""
    file_processed = ""
    for line in input_file:
        line = line[:line.find("\n")]
        if line.startswith("Model: "):
            #archive the previous model
            #Introduce a new model
            current_model = line[7:]
            if current_model not in results:
                results[current_model] = {}
            #reset filename
            file_processed = ""

        if line.startswith("File processed: "):
            #set the new file name
            file_processed = line[16:]
            if file_processed not in results[current_model]:
                results[current_model][file_processed] = {"accuracy": [[]], "energy": [-1], "memory": [[]], "f1": [[]]}
            else:
                results[current_model][file_processed]["accuracy"].append([])
                results[current_model][file_processed]["energy"].append(-1)
                results[current_model][file_processed]["memory"].append([])
                results[current_model][file_processed]["f1"].append([])

        if line.startswith("Accuracy: "):
            measure = line[9:]
            results[current_model][file_processed]["accuracy"][-1].append(measure.split("~"))
        if line.startswith("F1: "):
            measure = line[4:]
            results[current_model][file_processed]["f1"][-1].append(measure.split("~"))
        if line.startswith("Memory: "):
            measure = line[8:]
            results[current_model][file_processed]["memory"][-1].append(measure.split("~"))

        if line.startswith("\tTotal Energy:\t"):
            joule_index = line.find(" J", 15)
            results[current_model][file_processed]["energy"][-1] = line[15:joule_index]

    return results


def additional_computation(results):
    for model in results:
        for filename in results[model]:
            results[model][filename]["f1"] = aggregate_list_measurement(results[model][filename]["f1"])
            results[model][filename]["accuracy"] = aggregate_list_measurement(results[model][filename]["accuracy"])
            results[model][filename]["memory"] = aggregate_list_measurement(results[model][filename]["memory"])

    # model_name = "Mondrian Lifetime: 2 Base measure: 0.5 Discount factor: 0.2 Tree count: 10"
    for model in results:
        if model != "Empty":
            tmp = results[model]["/tmp/processed_subject1_ideal.log"]["accuracy"]
            x = [d[0] for d in tmp]
            plt.plot(x, [d[1] for d in tmp], label=model)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("perf_accuracy.png", bbox_inches="tight")
    plt.clf()

    for model in results:
        if model != "Empty":
            tmp = results[model]["/tmp/processed_subject1_ideal.log"]["f1"]
            x = [d[0] for d in tmp]
            plt.plot(x, [d[1] for d in tmp], label=model)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("perf_f1.png", bbox_inches="tight")
    plt.clf()

    for model in results:
        if model != "Empty":
            tmp = results[model]["/tmp/processed_subject1_ideal.log"]["memory"]
            x = [d[0] for d in tmp]
            plt.plot(x, [d[1] for d in tmp], label=model)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("memory.png", bbox_inches="tight")
    plt.clf()

    heights = [mean(map(float, results[model]["/tmp/processed_subject1_ideal.log"]["energy"])) for model in results]
    x = [model for model in results]
    plt.bar([i for i in range(len(x))], heights)
    plt.xticks([i for i in range(len(x))], x, rotation=90)


    plt.savefig("energy.png", bbox_inches="tight")

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
        run("/tmp/output")
    if sys.argv[1] == "dataset":
        dataset()
    if sys.argv[1] == "latex":
        latex()
    if sys.argv[1] == "process":
        results = process_output("/tmp/output")
        additional_computation(results)

