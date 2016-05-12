import json, itertools

import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import mannwhitneyu, ranksums, ttest_rel
from terminaltables import AsciiTable

rcParams['text.usetex'] = True

#Better to do a paired t-test

fetch = lambda filename: json.load(open(filename,'rb')).values()
format = lambda text: r'\Large \textbf{\textsc{%s}}'%text

def ordered_fetch(filename,order):
    db = json.load(open(filename,'rb'))
    return [db[o] for o in order]

order_of_names = ['%s-%s'%(rater_one,rater_two) for rater_one,rater_two 
        in itertools.combinations(open('../data/rater-names','rb').read().splitlines(),2)]
print order_of_names
#data = ['kappa-grades.json','lvsi-grades.json','lvsi-stains-grades.json','intra-rater-reliability.json']
data = ['../data/lvsi-grades-s-stains.json','../data/lvsi-grades-c-stains.json','../data/intra-rater-reliability.json']
ordered_data = [ordered_fetch(filename,order_of_names) for filename in data]
data = map(fetch,data)

#xlabels = ['Grading','-IHC','+IHC','Intra-rater']
xlabels = ['-IHC','+IHC','Intra-rater']

tbl = [[str(ranksums(datum,datum2).pvalue)
            for datum in data]
            for datum2 in data]

print AsciiTable([xlabels] + tbl).table

print data[0]
print ordered_data[0]

tbl = [[str(ttest_rel(datum,datum2).pvalue)
            for datum in ordered_data]
            for datum2 in ordered_data]

print AsciiTable([xlabels] + tbl).table


fig = plt.figure()
ax = fig.add_subplot(111)
bp = ax.boxplot(data, patch_artist=True,widths=0.5, notch=True)

for box in bp['boxes']:
    # change outline color
    box.set( color='k', linewidth=2)
    # change fill color
    box.set( facecolor = 'k',alpha=0.7 )

## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='k', linewidth=2)

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='k', linewidth=2)

## change color and linewidth of the medians
for median in bp['medians']:
    median.set(color='r', linewidth=2)

## change the style of fliers and their fill
for flier in bp['fliers']:
    flier.set(marker='o', color='k', alpha=0.5)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_position(('outward',10))
ax.spines['bottom'].set_position(('outward',10))
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.set_xticks(range(1,len(xlabels)+1))
ax.set_xticklabels(map(format,xlabels),rotation=60)
ax.set_ylabel(r'\Large $\mathbf{\kappa}$',rotation='horizontal',labelpad=20)
plt.tight_layout()
plt.savefig('../imgs/boxplot-notched-no-grading-notch.png')