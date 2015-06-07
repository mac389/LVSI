import json

import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import mannwhitneyu, ranksums
rcParams['text.usetex'] = True



fetch = lambda filename: json.load(open(filename,'rb')).values()
format = lambda text: r'\Large \textbf{\textsc{%s}}'%text

#data = ['kappa-grades.json','lvsi-grades.json','lvsi-stains-grades.json','intra-rater-reliability.json']
data = ['lvsi-grades.json','lvsi-stains-grades.json','intra-rater-reliability.json']
data = map(fetch,data)

#xlabels = ['Grading','-IHC','+IHC','Intra-rater']
xlabels = ['-IHC','+IHC','Intra-rater']
for i,datum in enumerate(data):
	for j,datum2 in enumerate(data):
		print '---------'
		print ranksums(datum,datum2)
		print xlabels[i],xlabels[j]
		print '--****-------'

fig = plt.figure()
ax = fig.add_subplot(111)
bp = ax.boxplot(data, patch_artist=True,notch=True,widths=0.5)

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
plt.savefig('boxplot-notched-no-grading.tiff')