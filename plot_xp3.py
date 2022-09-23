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
    f1s = f1s[(f1s['type'] == 'Stable') | (f1s['type'] == 'Add to fixed') | (f1s['type'] == 'Remove to fixed')]
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
def plot_bar(output_filename, used_names, legend_names, f1s):
    if used_names is None:
        used_names = sorted(list(set(f1s['name'])), reverse=True)
    if legend_names is None:
        legend_names = sorted(list(set(f1s['name'])), reverse=True)
    f1s = f1s[f1s['name'].isin(used_names)]
    names = used_names #sorted(list(set(f1s['name'])), reverse=True)
    colors = sns.color_palette('bright', len(names))
    palette = {z[0]:z[1] for z in zip(names, colors)}
    style = {k:'' for k in names}
    sizes = {k:2 for k in names}

    max_elts = f1s[['dataset', 'element_count']].groupby(['dataset']).max().reset_index()
    last_f1s = pd.merge(f1s, max_elts, on =['dataset', 'element_count'])
    last_f1s = last_f1s.rename(columns={'tree_count': 'Tree count'})
    #Split the one without and with tree counts
    best_tree_counts = last_f1s[last_f1s['Tree count'] <= 0]
    with_tree_count = last_f1s[last_f1s['Tree count'] > 0]
    #For the one without, get their best f1 combination
    best_tree_counts = best_tree_counts[['element_count', 'name', 'type', 'dataset', 'memory', 'real_dataset', 'Mean F1', 'f1 std']].groupby(['element_count', 'name', 'type', 'dataset', 'memory', 'real_dataset']).mean().reset_index()
    with_tree_count = with_tree_count[['element_count', 'name', 'type', 'dataset', 'memory', 'real_dataset', 'Mean F1', 'f1 std']].groupby(['element_count', 'name', 'type', 'dataset', 'memory', 'real_dataset']).max().reset_index()


    df = pd.concat([best_tree_counts, with_tree_count]).reset_index(drop=True)


    col_order = ['RandomRBF stable'] #, 'RandomRBF drift', 'Banos et al', 'Banos et al (drift)', 'Covtype', 'Recofit']
    # g = sns.FacetGrid(df, col='memory',  row='real_dataset')
    # g.map_dataframe(sns.barplot, x='name', y='Mean F1', hue_order=names, palette=palette)
    g = sns.catplot(data=df, x='Mean F1', y='name', hue='name', col='memory',  row='real_dataset', kind='bar', palette=palette, legend=False, dodge=False, order=used_names)


    # parent_mpl_figure = g.fig
    # g.add_legend()
    # lgd = parent_mpl_figure.legend(labels=legend_names, ncol=3, bbox_to_anchor=(0.5, 0.01, 0, 0), loc='upper center')
    g.set_titles('{row_name} - {col_name}MB')
    # g.set(xticks=[1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    # g.set(yticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    g.set_xticklabels(rotation=90)

    #Make it so there is one label every two ticks (for more space)
    # for ax in g.axes[0]:
        # ax.xaxis.set_ticklabels([])
        # ax.yaxis.set_ticklabels(['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'])
    plt.savefig(output_filename,
            dpi=100,
            # bbox_extra_artists=(lgd,),
            bbox_inches='tight')
def print_ranks(f1s):
    last_f1s = last_f1_score(f1s)
    datasets = sorted(list(set(last_f1s['dataset'])))
    memories = sorted(list(set(last_f1s['memory'])))
    names = sorted(list(set(last_f1s['name'])))

    ranking = dict([(name, {'rank':[], 'F1':[]}) for name in names])
    for dataset in datasets:
        for memory in memories:
            local_f1s = last_f1s[(last_f1s['memory'] == memory) & (last_f1s['dataset'] == dataset)]
            scores = [(row['name'], row['Mean F1'], row['f1 std']) for index, row in local_f1s.iterrows()]
            scores = sorted(scores, key=lambda x: x[1], reverse=True)
            for counter,row in enumerate(scores):
                ranking[row[0]]['rank'].append(counter)
                ranking[row[0]]['F1'].append(row[1])

    average_ranking = [(name, sum(ranks['rank'])/len(ranks['rank']), sum(ranks['F1'])/len(ranks['F1']))for name, ranks in ranking.items()]
    # average_ranking = [(name, median(ranks['rank']), median(ranks['F1']))for name, ranks in ranking.items()]
    average_ranking = sorted(average_ranking, key=lambda x: x[1])
    for rank in average_ranking:
        print(rank)

dataset_realname = {'RandomRBF_drift':'RandomRBF drift', 'RandomRBF_stable':'RandomRBF stable', 'banos_6':'Banos et al', 'covtype':'Covtype', 'drift_6':'Banos et al (drift)','recofit_6':'Recofit'}
datasets = ['RandomRBF_stable', 'RandomRBF_drift', 'banos_6', 'drift_6', 'recofit_6', 'covtype']
result_dir = 'results_xp3'

listy_f1 = []
# fname = 'mondrian_original_add_' + tree_count + '_to_' + tree_count + '_' + memory + 'M_ttf_' + trim_type + '_th_' + threshold_overfit + '_st_' + stats_type

# Load stable tree count
for dataset in datasets:
    f1_dir = result_dir + '/' + dataset
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


# Load Add from 1 to n
for dataset in datasets:
    f1_dir = result_dir + '/' + dataset
    for memory in ['0.2', '0.6', '10']:
        for trim_type in ['random', 'count', 'chop']:
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
                    fifi['real_dataset'] = dataset_realname[dataset]
                    listy_f1.append(fifi)
                except:
                    print('No file ' + f1_dir + '/' + fname + '.csv')

# Load delete from 50 to n
for dataset in datasets:
    f1_dir = result_dir + '/' + dataset
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
                    fifi['real_dataset'] = dataset_realname[dataset]
                    listy_f1.append(fifi)
                except:
                    print('No file ' + f1_dir + '/' + fname + '.csv')

# Load adaptive threshold
for dataset in datasets:
    f1_dir = result_dir + '/' + dataset
    for memory in ['0.2', '0.6', '10']:
        for threshold in ['z-test', 't-test', 'sum-std', 'sum-var', 'delta-sum-std']:
            for stats_type in ['fading', 'sliding']:
                for trim_type in ['count', 'random', 'chop']:
                    fname = 'mondrian_original_add_1_to_best_' + memory + 'M_ttf_' + trim_type + '_th_' + threshold + '_st_' + stats_type + '.csv'
                    try:
                        fifi = read_f1(f1_dir + '/' + fname)
                        fifi['name'] = trim_type + ' ' + stats_type + ' ' + threshold
                        fifi['type'] = 'Add to best'
                        fifi['stats_type'] = stats_type
                        fifi['Tree count'] = -1
                        fifi['dataset'] = dataset
                        fifi['memory'] = memory
                        fifi['threshold_overfit'] = threshold
                        fifi['real_dataset'] = dataset_realname[dataset]
                        listy_f1.append(fifi)
                    except Exception as e:
                        print('No file R ' + f1_dir + '/' + fname)


only_df = pd.concat(listy_f1).reset_index(drop=True)
last_f1 = last_f1_score(only_df)

plot_tree_count('f1_tree_count.pdf', None, None, last_f1[(last_f1['dataset'] != 'RandomRBF_drift') & (last_f1['dataset'] != 'drift_6')])
plot_tree_variation('f1_add_remove.pdf', None, None, last_f1[(last_f1['dataset'] == 'banos_6') | (last_f1['dataset'] == 'RandomRBF_stable')])
plot_tree_variation('f1_add_remove_full.pdf', None, None, last_f1)

print('==== Fading ====')
print_ranks(last_f1[last_f1['stats_type'] == 'fading'])
print('==== Sliding ====')
print_ranks(last_f1[last_f1['stats_type'] == 'sliding'])
print('==== Fading vs Sliding ====')
print_ranks(last_f1[(last_f1['stats_type'] == 'sliding') | (last_f1['stats_type'] == 'fading')])
print('==== Global ====')
print_ranks(last_f1[~last_f1['stats_type'].isnull()])

names = ['Stable', 'count sliding sum-var', 'random sliding sum-var', 'count fading sum-std', 'count fading sum-var', 'count fading t-test', 'count sliding t-test']
plot_bar('xp3.pdf', names, names, last_f1)
