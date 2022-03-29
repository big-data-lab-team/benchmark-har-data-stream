#!/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
from f1_utils import read_f1
import copy
def cmp(a):
    return float(a[1]) - float(a[2])

f1_dir = 'results_xp2'
output_dir = 'draft_22'
loutry_f1 = []
dataset_realname = {'RandomRBF_drift':'RandomRBF drift', 'RandomRBF_stable':'RandomRBF stable', 'banos_6':'Banos et al', 'covtype':'Covtype', 'drift_6':'Banos et al (drift)','recofit_6':'Recofit'}

plt.rcParams.update({'font.size': 27})
for dataset in ['RandomRBF_drift', 'RandomRBF_stable', 'banos_6', 'covtype', 'drift_6','recofit_6']:
# for dataset in ['banos_6']:
    d = f1_dir + '/' + dataset
    listy_f1 = []
    for t in ['1', '5', '10', '20', '30', '50']:
        fifi = read_f1(d + '/mondrian_unbound_t' + t + '_original.csv')
        fifi['name'] = 'Mondrian 2GB'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        fifi['memory'] = '2GB'
        listy_f1.append(fifi)

        fifi = read_f1(d + '/mondrian_t' + t + '_original_none_none.csv')
        fifi['name'] = 'No Trim'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        fifi['memory'] = '600KB'
        listy_f1.append(fifi)

        fifi = read_f1(d + '/mondrian_t' + t + '_original_none_count.csv')
        fifi['name'] = 'Trim Count, No Split'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        fifi['memory'] = '600KB'
        listy_f1.append(fifi)

        fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_avg_count.csv')
        fifi['name'] = 'Trim Count, Split AVG'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        fifi['memory'] = '600KB'
        listy_f1.append(fifi)

        fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_weighted_count.csv')
        fifi['name'] = 'Trim Count, Split Barycenter'
        fifi['tree_count'] = int(t)
        fifi['dataset'] = copy.copy(dataset)
        fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        fifi['memory'] = '600KB'
        listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_avg_fading_score.csv')
        # fifi['name'] = 'Trim Fading, Split AVG'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
		# fifi['memory'] = '600KB'
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_weighted_fading_score.csv')
        # fifi['name'] = 'Trim Fading, Split Barycenter'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
		# fifi['memory'] = '600KB'
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_original_none_fading_score.csv')
        # fifi['name'] = 'Trim Fading, No Split'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # fifi['memory'] = '600KB'
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_original_none_random.csv')
        # fifi['name'] = 'Trim Random, No Split'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # fifi['memory'] = '600KB'
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_avg_random.csv')
        # fifi['name'] = 'Trim Random, Split AVG'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # fifi['memory'] = '600KB'
        # listy_f1.append(fifi)

        # fifi = read_f1(d + '/mondrian_t' + t + '_barycenter_weighted_random.csv')
        # fifi['name'] = 'Trim Random, Split Barycenter'
        # fifi['tree_count'] = int(t)
        # fifi['dataset'] = copy.copy(dataset)
        # fifi['real_dataset'] = copy.copy(dataset_realname[dataset])
        # fifi['memory'] = '600KB'
        # listy_f1.append(fifi)



    loutry_f1.extend(listy_f1)
    f1s = pd.concat(listy_f1).reset_index(drop=True)
    names = sorted(list(set(f1s['name'])))
    colors = sns.color_palette('tab10', len(names))
    palette = {z[0]:z[1] for z in zip(names, colors)}
    max_elts = f1s[['dataset', 'element_count']].groupby(['dataset']).max().reset_index()
    lf1s = pd.merge(f1s, max_elts, on =['dataset', 'element_count'])
    list_last_f1s= [(row['name'], row['tree_count'], row['Mean F1']) for index, row in lf1s.iterrows()]
    list_last_f1s = sorted(list_last_f1s, key=cmp)
    print('========== ' + dataset + ' ===========')
    for e in list_last_f1s:
        print(str(e[1]) + ' - ' + str(e[0]) + ' : ' + str(e[2]))

    # g = sns.relplot(
            # data=f1s, x='element_count', y='Mean F1',
            # col='tree_count', hue='name',
            # col_wrap=2, palette=palette,
            # kind='line'
            # )
    # g.fig.suptitle(dataset)
    # leg = g._legend
    # leg.set_bbox_to_anchor([1.0,0.5])
    # leg.set(frame_on=True)
    # plt.savefig(output_dir + '/' + dataset + '.pdf', bbox_extra_artists=(leg,), bbox_inches='tight', dpi=48*5)
    # plt.cla()
    # plt.clf()

f1s = pd.concat(loutry_f1).reset_index(drop=True)
names = ['Mondrian 2GB', 'No Trim', 'Trim Count, Split AVG', 'Trim Count, Split Barycenter', 'Trim Count, No Split', 'Trim Fading, Split AVG', 'Trim Fading, Split Barycenter', 'Trim Fading, No Split', 'Trim Random, Split AVG', 'Trim Random, Split Barycenter', 'Trim Random, No Split', 'Mondrian 2GB']
colors = sns.color_palette('bright', len(names)-1)
palette = {z[0]:z[1] for z in zip(names[1:], colors)}
palette['Mondrian 2GB'] = '#000000'
# palette['Trim Random, Extend'] = '#FF0256'
style = {k:'' for k in names}
style['Mondrian 2GB'] = (4, 1.5)

max_elts = f1s[['dataset', 'element_count']].groupby(['dataset']).max().reset_index()
last_f1s = pd.merge(f1s, max_elts, on =['dataset', 'element_count'])
col_order = ['RandomRBF stable', 'RandomRBF drift', 'Banos et al', 'Banos et al (drift)', 'Covtype', 'Recofit']
last_f1s = last_f1s.rename(columns={'tree_count': 'Tree count'})
g = sns.relplot(
        data=last_f1s, x='Tree count', y='Mean F1',
        col='real_dataset', hue='name', palette=palette,
        col_wrap=2, col_order=col_order, legend=True,
		# style='memory', style_order=['600KB', '2GB'],
        style='name', dashes=style,
        kind='line'
        )
g.set_titles('{col_name}')
g.set(xticks=[1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
g.set(yticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
for ax in g.axes:
    ax.yaxis.set_ticklabels(['0.1', '', '0.3', '', '0.5', '', '0.7', '', '0.9'])
    ax.xaxis.set_ticklabels(['1', '', '10', '', '20', '', '30', '', '40', '', '50'])
plt.show()

loutre = f1s[(f1s['dataset'] == 'RandomRBF_stable') & (f1s['tree_count'] == 5)]
sns.lineplot(data=loutre, x='element_count', y='Mean F1', hue='name', palette=palette, legend=True)
plt.show()