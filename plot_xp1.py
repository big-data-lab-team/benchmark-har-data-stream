#!/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn import metrics
import sys
import copy
from f1_utils import read_f1

f1_dir = 'results_xp1'
datasets = ['recofit_6', 'covtype', 'drift_6', 'banos_6', 'RandomRBF_stable', 'RandomRBF_drift']
dataset_realname = {'RandomRBF_drift':'RandomRBF drift', 'RandomRBF_stable':'RandomRBF stable', 'banos_6':'Banos et al', 'covtype':'Covtype', 'drift_6':'Banos et al (drift)','recofit_6':'Recofit'}

loutry_f1 = []
plt.rcParams.update({'font.size': 27})
for dataset in datasets:
    listy_f1 = []
    d = f1_dir + '/' + dataset
    for t in ['1', '5', '10', '20', '30', '50']:
        fifi = read_f1(d + '/mondrian_unbound_t' + t + '_original.csv')
        fifi['name'] = 'Mondrian 2GB'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        listy_f1.append(fifi)

        fifi = read_f1(d + '/mondrian_t' + t + '_none.csv')
        fifi['name'] = 'Stopped'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        listy_f1.append(fifi)

        fifi = read_f1(d + '/mondrian_t' + t + '_original.csv')
        fifi['name'] = 'Extend Node'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        listy_f1.append(fifi)

        fifi = read_f1(d + '/mondrian_t' + t + '_partial.csv')
        fifi['name'] = 'Partial Update'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        listy_f1.append(fifi)

        fifi = read_f1(d + '/mondrian_t' + t + '_count_only.csv')
        fifi['name'] = 'Count Only'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        listy_f1.append(fifi)

        fifi = read_f1(d + '/mondrian_t' + t + '_ghost.csv')
        fifi['name'] = 'Ghost'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        listy_f1.append(fifi)


    # d = 'results_xp2' + '/' + dataset
    # for t in ['1', '5', '10', '20', '30', '50']:
        # fifi = read_f1(d + '/mondrian_t' + t + '_original_none_count.csv')
        # fifi['name'] = 'Trim Count, Extend'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_avg_count.csv')
        # fifi['name'] = 'Trim Counts, Split AVG'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_weighted_count.csv')
        # fifi['name'] = 'Trim Counts, Split Barycenter'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # listy_f1.append(fifi)


        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_avg_fading_score.csv')
        # fifi['name'] = 'Trim Fading, Split AVG'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_weighted_fading_score.csv')
        # fifi['name'] = 'Trim Fading, Split Barycenter'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_original_none_fading_score.csv')
        # fifi['name'] = 'Trim Fading, Extend'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_original_none_random.csv')
        # fifi['name'] = 'Trim Random, Extend'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_avg_random.csv')
        # fifi['name'] = 'Trim Random, Split AVG'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_weighted_random.csv')
        # fifi['name'] = 'Trim Random, Split Barycenter'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # listy_f1.append(fifi)


    loutry_f1.extend(listy_f1)
    # f1s = pd.concat(listy_f1).reset_index(drop=True)
    # names = sorted(list(set(f1s['name'])))
    # colors = sns.color_palette('deep', len(names))
    # palette = {z[0]:z[1] for z in zip(names, colors)}

    # max_elts = f1s[['dataset', 'element_count']].groupby(['dataset']).max().reset_index()
    # lf1s = pd.merge(f1s, max_elts, on =['dataset', 'element_count'])
    # list_last_f1s= [(row['name'], row['tree_count'], row['Mean F1']) for index, row in lf1s.iterrows()]
    # # list_last_f1s = sorted(list_last_f1s, key=cmp)
    # list_last_f1s = sorted(list_last_f1s)
    # print('========== ' + dataset + ' ===========')
    # for e in list_last_f1s:
        # print(str(e[1]) + ' - ' + str(e[0]) + ' : ' + str(e[2]))

f1s = pd.concat(loutry_f1).reset_index(drop=True)
#Keep order for colors and name with a palette
# names = sorted(list(set(f1s['name'])))
names = ['Mondrian 2GB', 'Stopped', 'Extend Node', 'Partial Update', 'Count Only', 'Ghost']
colors = sns.color_palette('bright', len(names)-1)
palette = {z[0]:z[1] for z in zip(names[1:], colors)}
palette['Mondrian 2GB'] = '#000000'
style = {k:'' for k in names}
style['Mondrian 2GB'] = (4, 1.5)

#Keep only last element for the f1-score
max_elts = f1s[['dataset', 'element_count']].groupby(['dataset']).max().reset_index()
last_f1s = pd.merge(f1s, max_elts, on =['dataset', 'element_count'])
col_order = ['RandomRBF stable', 'RandomRBF drift', 'Banos et al', 'Banos et al (drift)', 'Covtype', 'Recofit']

last_f1s = last_f1s.rename(columns={'tree_count': 'Tree count'})
g = sns.relplot(
        data=last_f1s, x='Tree count', y='Mean F1',
        col='real_dataset', hue='name', palette=palette,
        col_wrap=2, col_order=col_order,
        style='name', dashes=style,
        kind='line', legend=True
        )
g.set_titles('{col_name}')
g.set(xticks=[1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
g.set(yticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
for ax in g.axes:
    ax.yaxis.set_ticklabels(['0.1', '', '0.3', '', '0.5', '', '0.7', '', '0.9'])
    ax.xaxis.set_ticklabels(['1', '', '10', '', '20', '', '30', '', '40', '', '50'])

# g.set(yticklabels=[0.1, 0.3, 0.5, 0.7, 0.9])
plt.show()

# baseline = last_f1s[last_f1s['name'] == 'Stopped Mondrian']
# baseline = baseline[['Mean F1', 'dataset', 'tree_count']]
# baseline.columns = ['Baseline F1', 'dataset', 'tree_count']
# last_f1s = pd.merge(last_f1s, baseline, on=['dataset', 'tree_count'])
# last_f1s['Delta F1'] = last_f1s['Mean F1'] - last_f1s['Baseline F1']
# f1s_no_stopped = last_f1s[last_f1s['name'] != 'Stopped Mondrian']


# delta_stats = f1s_no_stopped[['name', 'real_dataset', 'Delta F1']].groupby(['real_dataset', 'name']).agg(['min', 'mean', 'max'])
## delta_stats = f1s_no_stopped[['name', 'Delta F1']].groupby(['name']).agg(['min', 'mean', 'max'])
# delta_stats = delta_stats.round(2)
# pd.set_option('min_rows', 78)
# print(delta_stats)
# delta_stats.columns = ['name', 'dataset', 'min', 'mean', 'max']
