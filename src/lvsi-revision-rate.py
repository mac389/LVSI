import itertools, json

import pandas as pd
import numpy as np 
from awesome_print import ap 
from statsmodels.stats.inter_rater import cohens_kappa, to_table

pathologists = open('rater-names','rb').read().splitlines()

kappas = {}
contingency_table = np.zeros((len(pathologists),3,3))
for j,pathologist in enumerate(pathologists):

	lvsi_no_ihc = pd.read_excel('no-stain.xls',pathologist,parse_cols=[1,2,3], convert_float=False)
 	lvsi_yes_ihc = pd.read_excel('stains.xls',pathologist,parse_cols=[1,2,3], convert_float=False)

	lvsi_no_ihc_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in lvsi_no_ihc.apply(np.nonzero,axis=1).values]).astype(int)
	lvsi_yes_ihc_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in lvsi_yes_ihc.apply(np.nonzero,axis=1).values]).astype(int)

	for rating_one ,rating_two in zip(lvsi_no_ihc_ratings,lvsi_yes_ihc_ratings):
		if type(rating_one) == type(list):
			rating_one = rating_one[0]
		if type(rating_two) == type(list):
			rating_two = rating_two[0]
			print '\t %d'%rating_two
		contingency_table[j,rating_one,rating_two] += 1

	print contingency_table[j,:,:]
	print pathologist
	#json.dump(kappas,open('kappa-grades.json','wb'))

print np.median(contingency_table,axis=0)
print 0.5*(np.percentile(contingency_table,75,axis=0) - np.percentile(contingency_table,25,axis=0))
print contingency_table[:,0,2]
#ap(np.median(kappas.values()))
#print 0.5*(np.percentile(kappas.values(),75)-np.percentile(kappas.values(),25))