#!/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn import metrics
import sys
import copy
from f1_utils import read_f1

def plot_names(output_filename, used_names, legend_names, f1s):
    f1s = f1s[f1s['name'].isin(used_names)]
    names = ['Online Mondrian', 'Data Stream Mondrian 2GB', 'Stopped', 'Extend Node', 'Partial Update', 'Count Only', 'Ghost']
    colors = sns.color_palette('bright', len(names)-1)
    palette = {z[0]:z[1] for z in zip(names[2:], colors)}
    palette['Data Stream Mondrian 2GB'] = '#000000'
    palette['Online Mondrian'] = '#FF0000'
    style = {k:'' for k in names}
    style['Data Stream Mondrian 2GB'] = (4, 6)
    style['Online Mondrian'] = (4, 6)
    sizes = {k:4 for k in names}

    max_elts = f1s[['dataset', 'element_count']].groupby(['dataset']).max().reset_index()
    last_f1s = pd.merge(f1s, max_elts, on =['dataset', 'element_count'])
    col_order = ['RandomRBF stable', 'RandomRBF drift', 'Banos et al', 'Banos et al (drift)', 'Covtype', 'Recofit']
    last_f1s = last_f1s.rename(columns={'tree_count': 'Tree count'})
    g = sns.relplot(
            data=last_f1s, x='Tree count', y='Mean F1',
            col='real_dataset', hue='name', palette=palette,
            col_wrap=2, col_order=col_order, legend=False,
            style='name', dashes=style,
            size='name', sizes=sizes,
            aspect=3,
            kind='line')
    parent_mpl_figure = g.fig
    lgd = parent_mpl_figure.legend(labels=legend_names, ncol=3, bbox_to_anchor=(0.5, 0.01, 0, 0), loc='upper center')
    g.set_titles('{col_name}')
    g.set(xticks=[1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    g.set(yticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

    #Make it so there is one label every two ticks (for more space)
    for ax in g.axes:
        ax.yaxis.set_ticklabels(['0.1', '', '0.3', '', '0.5', '', '0.7', '', '0.9'])
        ax.xaxis.set_ticklabels(['1', '', '10', '', '20', '', '30', '', '40', '', '50'])
    plt.savefig(output_filename,
            dpi=100,
            bbox_extra_artists=(lgd,),
            bbox_inches='tight')

online_mondrian_forest_scores = {'banos_6' : {1: 0.68, 5:0.82, 10:0.86, 20:0.88, 30:0.89, 40:0.89, 50:0.89},
 'drift_6' : {1: 0.35, 5:0.43, 10:0.43, 20:0.45, 30:0.45, 40:0.45, 50:0.44},
 'RandomRBF_stable' : {1: 0.78, 5:0.87, 10:0.88, 20:0.90, 30:0.90, 40:0.90, 50:0.90},
 'RandomRBF_drift' : {1: 0.41, 5:0.60, 10:0.66, 20:0.70, 30:0.71, 40:0.71, 50:0.72},
 'covtype' : {1: 0.81, 5:0.88, 10:0.90, 20:0.91, 30:0.91, 40:0.91, 50:0.91},
 'recofit_6' : {1: 0.50, 5:0.68, 10:0.74, 20:0.766, 30:0.77, 40:0.78, 50:0.78}
 }
online_df = {
        'Mean F1' : [],
        'f1 std' : [],
        'name' : [],
        'tree_count' : [],
        'dataset' : [],
        'real_dataset' : [],
        'memory' : []
        }
f1_dir = 'results_xp1'
datasets = ['recofit_6', 'covtype', 'drift_6', 'banos_6', 'RandomRBF_stable', 'RandomRBF_drift']
dataset_realname = {'RandomRBF_drift':'RandomRBF drift', 'RandomRBF_stable':'RandomRBF stable', 'banos_6':'Banos et al', 'covtype':'Covtype', 'drift_6':'Banos et al (drift)','recofit_6':'Recofit'}
memory_name = {'0.6M':600000, '1M':1000000, '10M':10000000, '50M':50000000, '100M':100000000, '200M':200000000, '2GB' : 2000000000}

#Read the data
list_f1_data = []
plt.rcParams.update({'font.size': 27})
for dataset in datasets:
    listy_f1 = []
    d = f1_dir + '/' + dataset
    for t in ['1', '5', '10', '20', '30', '50']:
        online_df['Mean F1'].append(online_mondrian_forest_scores[dataset][int(t)])
        online_df['f1 std'].append(0.0)
        online_df['name'].append('Online Mondrian')
        online_df['memory'].append(-1)
        online_df['tree_count'].append(int(t))
        online_df['dataset'].append(copy.copy(dataset))
        online_df['real_dataset'].append(copy.copy(dataset_realname[dataset]))

        fifi = read_f1(d + '/mondrian_unbound_t' + t + '_original.csv')
        fifi['name'] = 'Data Stream Mondrian 2GB'
        fifi['memory'] = memory_name['2GB']
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        list_f1_data.append(fifi)

        for memory in ['0.6M']:
            fifi = read_f1(d + '/mondrian_t' + t + '_none_' + memory + '.csv')
            fifi['name'] = 'Stopped'
            fifi['memory'] = memory_name[memory]
            fifi['tree_count'] = int(t)
            fifi['dataset'] = copy.copy(dataset)
            fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
            list_f1_data.append(fifi)

            fifi = read_f1(d + '/mondrian_t' + t + '_original_' + memory + '.csv')
            fifi['name'] = 'Extend Node'
            fifi['memory'] = memory_name[memory]
            fifi['tree_count'] = int(t)
            fifi['dataset'] = copy.copy(dataset)
            fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
            list_f1_data.append(fifi)

            fifi = read_f1(d + '/mondrian_t' + t + '_partial_' + memory + '.csv')
            fifi['name'] = 'Partial Update'
            fifi['memory'] = memory_name[memory]
            fifi['tree_count'] = int(t)
            fifi['dataset'] = copy.copy(dataset)
            fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
            list_f1_data.append(fifi)

            fifi = read_f1(d + '/mondrian_t' + t + '_count_only_' + memory + '.csv')
            fifi['name'] = 'Count Only'
            fifi['memory'] = memory_name[memory]
            fifi['tree_count'] = int(t)
            fifi['dataset'] = copy.copy(dataset)
            fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
            list_f1_data.append(fifi)

            fifi = read_f1(d + '/mondrian_t' + t + '_ghost_' + memory + '.csv')
            fifi['name'] = 'Ghost'
            fifi['memory'] = memory_name[memory]
            fifi['tree_count'] = int(t)
            fifi['dataset'] = copy.copy(dataset)
            fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
            list_f1_data.append(fifi)

f1s = pd.concat(list_f1_data).reset_index(drop=True)
max_elts = f1s[['element_count', 'dataset']].groupby(['dataset']).max().reset_index()
of1 = pd.DataFrame(online_df)
of1 = pd.merge(of1, max_elts, on =['dataset'])
cols = ['element_count', 'Mean F1', 'f1 std', 'name', 'tree_count', 'dataset' , 'real_dataset', 'memory']
of1 = of1[cols]

f1s = pd.concat([of1, f1s]).reset_index(drop=True)
plot_names('xp1.pdf',
        ['Online Mondrian', 'Data Stream Mondrian 2GB', 'Stopped', 'Extend Node', 'Partial Update', 'Count Only', 'Ghost'],
        ['Online Mondrian', 'Data Stream Mondrian 2GB', 'Stopped', 'Extend Node', 'Partial Update', 'Count Only', 'Ghost'],
        f1s[(f1s['memory'] == memory_name['0.6M']) | (f1s['memory'] == memory_name['2GB']) | (f1s['memory'] < 0)])

