import os
import csv
import statistics, re
import pandas as pd #yes
import seaborn as sns
from statistics import mean
import matplotlib.pyplot as plt #yes
def hashStringToColor(string):
    hsh = hash(string)
    r = (hsh & 0xFF0000) >> 16
    g = (hsh & 0x00FF00) >> 8
    b = hsh & 0x0000FF
    return "#" + format(r, "02x") + format(g, "02x") + format(b, "02x")

def process_output(output_filename, run_output_filename, model_filename):
    def add_names(row, models):
        key = str(int(row['model_id']))
        name = models[key]['name']
        ##### CHANGE HERE TO CHANGE FULLNAME ######
        if name == 'Mondrian':
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
    ####### Controlling the datasets 1/4 ########
    dataset_title = {'banos_3': 'Banos et al', 'recofit_3': 'Recofit', 'drift_3': 'Banos et al (Drift)', 'dataset_1': 'Hyperplane', 'dataset_2' : 'RandomRBF', 'dataset_3' : 'RandomTree', 'banos_6': 'Banos et al, 6 axis', 'recofit_6': 'Recofit 6 axis', 'drift_6' : 'Banos et al 6 axis (Drift)'}
    #dataset_title = {'banos_3': 'Banos et al', 'banos_6': 'Banos et al, 6 axis'}
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
    ####### Controlling the datasets 2/4 ########
    knn_offline_f1 = {'banos_3': 0.0, 'recofit_3': 0.0, 'drift_3': 0.0, 'dataset_1': 0.95, 'dataset_2' : 0.78, 'dataset_3' : 0.69, 'banos_6': 0.86, 'recofit_6': 0.40, 'drift_6' : 0.86}
    #knn_offline_f1 = {'banos_3': 0.0, 'banos_6': 0.86}
    print(names)
    print(colors)
    print(markers)
    print(styles)
    plt.rcParams.update({'font.size': 33})
    ####### Controlling the datasets 3/4 ########
    list_datastets = ['banos_6', 'drift_3', 'banos_3', 'recofit_3', 'dataset_1', 'dataset_2', 'dataset_3', 'drift_6', 'recofit_6']
    #list_datastets = ['banos_6', 'drift_3', 'banos_3', 'recofit_3', 'dataset_1', 'dataset_2', 'dataset_3', 'drift_6', 'dataset_2', 'recofit_6']
    #list_datastets = ['banos_6', 'banos_3']
    for dataset_name in list_datastets:
        print('Dataset: ' + dataset_name)

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
            # if len(daty[daty.fullname == name]['f1']) > 0:
                # print(name+" - " + str(list(daty[daty.fullname == name]['f1'])[-1]))

        if dataset_name in knn_offline_f1:
            x = [a for a in daty[daty.fullname == name]['element_count']]
            y = [knn_offline_f1[dataset_name] for a in daty[daty.fullname == name]['element_count']]
            plt.plot(x, y, color='#000000', linestyle='-.', label='kNN Offline')

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

            # plt.plot(x, zeross, color='#000000', linestyle='-.', label='kNN Offline')
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
            plt.fill_between(daty_std[daty_std.fullname == name]['element_count'], y1, y2, color=color, linestyle=style, alpha=0.15)
        if dataset_name in knn_offline_f1:
            x = [a for a in daty[daty.fullname == name]['element_count']]
            y = [knn_offline_f1[dataset_name] for a in daty[daty.fullname == name]['element_count']]
            plt.plot(x, y, color='#000000', linestyle='-.', label='kNN Offline')
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
#main driver
dir_name = 'results'
output_lst, output_run_lst, models_lst = [], [], []
PRECISIONS = [1,2]
for i in PRECISIONS:
    output, output_runs, models = process_output(dir_name+"/output_"+str(i),dir_name+"/output_runs_"+str(i),dir_name+"/models_"+str(i)+".csv")
    output_lst.append(output)
    output_run_lst.append(output_runs)
    models_lst.append(models)
if not os.path.exists("verificarlo_plotting"):
    os.mkdir("verificarlo_plotting")
print_results(output_lst, output_runs_lst, models_lst, output_directory='verificarlo_plotting')
