#!/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn import metrics
import sys
import copy
from f1_utils import read_f1

def last_f1_score(f1s):
    max_elts = f1s[['dataset', 'element_count']].groupby(['dataset']).max().reset_index()
    last_f1s = pd.merge(f1s, max_elts, on =['dataset', 'element_count'])
    return last_f1s
def plot_tree_count(output_filename, used_names, legend_names, f1s):
    f1s = f1s[f1s['type'] == 'Stable']
    names = sorted(list(set(f1s['name'])), reverse=True)
    colors = sns.color_palette('bright', len(names))
    palette = {z[0]:z[1] for z in zip(names, colors)}
    style = {k:'' for k in names}
    sizes = {k:2 for k in names}

    legend_names = [str(j) for j in sorted([float(i) for i in set(f1s['memory'])])]

    col_order = ['RandomRBF stable', 'RandomRBF drift', 'Banos et al', 'Banos et al (drift)', 'Covtype', 'Recofit']
    col_order = ['RandomRBF stable', 'Banos et al', 'Covtype', 'Recofit']
    g = sns.relplot(
            data=f1s, x='Tree count', y='Mean F1',
            size='name', sizes=sizes,
            col_wrap=2, col='real_dataset', col_order=col_order,
            hue='memory', kind='line',
            legend=False)

    parent_mpl_figure = g.fig
    lgd = parent_mpl_figure.legend(labels=legend_names, ncol=3, bbox_to_anchor=(0.5, 0.01, 0, 0), loc='upper center')
    g.set_titles('{col_name}')
    g.set(xticks=[1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    g.set(yticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

    #Make it so there is one label every two ticks (for more space)
    for ax in g.axes:
        ax.xaxis.set_ticklabels(['1', '', '10', '', '20', '', '30', '', '40', '', '50'])
        ax.yaxis.set_ticklabels(['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'])
    plt.savefig(output_filename,
            dpi=100,
            bbox_extra_artists=(lgd,),
            bbox_inches='tight')
def plot_tree_variation(output_filename, used_names, legend_names, f1s):
    names = sorted(list(set(f1s['name'])), reverse=True)
    colors = sns.color_palette('bright', len(names))
    palette = {z[0]:z[1] for z in zip(names, colors)}
    style = {k:'' for k in names}
    sizes = {k:2 for k in names}

    col_order = ['RandomRBF stable', 'RandomRBF drift', 'Banos et al', 'Banos et al (drift)', 'Covtype', 'Recofit']
    g = sns.relplot(
            data=f1s, x='Tree count', y='Mean F1',
            palette=palette,
            hue='name', hue_order=names,
            size='name', sizes=sizes,
            col='memory', row='real_dataset',
            kind='line',
            legend=True)

    parent_mpl_figure = g.fig
    # lgd = parent_mpl_figure.legend(labels=names, ncol=3, bbox_to_anchor=(0.5, 0.01, 0, 0), loc='upper center')
    g.set_titles('{col_name} - {row_name}')
    g.set(xticks=[1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    g.set(yticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

    #Make it so there is one label every two ticks (for more space)
    for axes in g.axes:
        for ax in axes:
            ax.xaxis.set_ticklabels(['1', '', '10', '', '20', '', '30', '', '40', '', '50'])
            ax.yaxis.set_ticklabels(['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'])
    plt.savefig(output_filename,
            dpi=100,
            # bbox_extra_artists=(lgd,),
            bbox_inches='tight')

dataset_realname = {'RandomRBF_drift':'RandomRBF drift', 'RandomRBF_stable':'RandomRBF stable', 'banos_6':'Banos et al', 'covtype':'Covtype', 'drift_6':'Banos et al (drift)','recofit_6':'Recofit'}

listy_f1 = []
# fname = 'mondrian_original_add_' + tree_count + '_to_' + tree_count + '_' + memory + 'M_ttf_' + trim_type + '_th_' + threshold_overfit + '_st_' + stats_type

for dataset in ['RandomRBF_stable', 'banos_6', 'drift_6', 'recofit_6', 'covtype', 'RandomRBF_drift']:
    f1_dir = 'results_xp3/' + dataset
    for memory in ['0.2', '0.6', '10']:
        for tree_count in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '20', '25', '30', '35', '40', '45', '50']:
            fname = 'mondrian_original_add_' + tree_count + '_to_' + tree_count + '_' + memory + 'M_ttf_none_th_-1_st_none'
            fifi = read_f1(f1_dir + '/' + fname + '.csv')
            fifi['name'] = 'Stable'
            fifi['type'] = 'Stable'
            fifi['Tree count'] = int(tree_count)
            fifi['dataset'] = dataset
            fifi['memory'] = memory
            fifi['threshold_overfit'] = -1
            fifi['real_dataset'] = dataset_realname[dataset]
            listy_f1.append(fifi)

# for dataset in ['RandomRBF_stable', 'banos_6']:
for dataset in ['RandomRBF_stable', 'banos_6', 'drift_6', 'recofit_6', 'covtype', 'RandomRBF_drift']:
    f1_dir = 'results_xp3/' + dataset
    for memory in ['0.2', '0.6', '10']:
        for trim_type in ['random', 'count']:
            for tree_count in ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '20']:
                fname = 'mondrian_original_add_1_to_' + tree_count + '_' + memory + 'M_ttf_' + trim_type + '_th_-1_st_none'
                try:
                    fifi = read_f1(f1_dir + '/' + fname + '.csv')
                    fifi['name'] = 'Add ' + trim_type
                    fifi['type'] = 'Add to fixed'
                    fifi['Tree count'] = int(tree_count)
                    fifi['dataset'] = dataset
                    fifi['memory'] = memory
                    fifi['threshold_overfit'] = -1
                    fifi['maximum_trim_size'] = 0.03
                    fifi['real_dataset'] = dataset_realname[dataset]
                    listy_f1.append(fifi)
                except:
                    print('No file ' + f1_dir + '/' + fname + '.csv')

for dataset in ['RandomRBF_stable', 'banos_6', 'drift_6', 'recofit_6', 'covtype', 'RandomRBF_drift']:
    f1_dir = 'results_xp3/' + dataset
    for memory in ['0.2', '0.6', '10']:
        for trim_type in ['random', 'count']:
            for tree_count in ['45', '40', '35', '30', '25', '20']:
                fname = 'mondrian_original_add_50_to_' + tree_count + '_' + memory + 'M_ttf_none_th_-1_st_none'
                try:
                    fifi = read_f1(f1_dir + '/' + fname + '.csv')
                    fifi['name'] = 'Remove'
                    fifi['type'] = 'Remove to fixed'
                    fifi['Tree count'] = int(tree_count)
                    fifi['dataset'] = dataset
                    fifi['memory'] = memory
                    fifi['threshold_overfit'] = -1
                    fifi['maximum_trim_size'] = 0.03
                    fifi['real_dataset'] = dataset_realname[dataset]
                    listy_f1.append(fifi)
                except:
                    print('No file ' + f1_dir + '/' + fname + '.csv')

only_df = pd.concat(listy_f1).reset_index(drop=True)
last_f1 = last_f1_score(only_df)

plot_tree_count('f1_tree_count.pdf', None, None, last_f1[(last_f1['dataset'] != 'RandomRBF_drift') & (last_f1['dataset'] != 'drift_6')])
# plot_tree_variation('f1_tree_count.pdf', None, None, last_f1[(last_f1['dataset'] == 'banos_6') | (last_f1['dataset'] == 'RandomRBF_stable')])
# plot_tree_variation('f1_tree_count.pdf', None, None, last_f1)
