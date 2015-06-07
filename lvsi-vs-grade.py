import itertools, json

import pandas as pd
import numpy as np 
from awesome_print import ap 
from statsmodels.stats.inter_rater import cohens_kappa, to_table

possible_grades = ['1','2','3']
cols_with_grades = [4,5,6]
cols_with_lvsi = [1,2,3]
pathologists = open('rater-names','rb').read().splitlines()

kappas = {}
contingency_table = np.zeros((len(pathologists),3,3)).astype(int)


for j,pathologist in enumerate(pathologists):

	histology_grade = pd.read_excel('no-stain.xls',pathologist,parse_cols=cols_with_grades,convert_float=False)
	lvsi = pd.read_excel('no-stain.xls',pathologist,parse_cols=cols_with_lvsi,convert_float=False)

	histology_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in histology_grade.apply(np.nonzero,axis=1).values]).astype(int)
	lvsi_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in lvsi.apply(np.nonzero,axis=1).values]).astype(int)

	for histolog_rating,lvsi_rating in zip(histology_ratings,lvsi_ratings):
		#print rating_one,rating_two
		if type(histolog_rating) == type(list):
			histology_rating = histolog_rating[0]
		if type(lvsi_rating) == type(list):
			lvsi_rating = lvsi_rating[0]
		#print i 
		contingency_table[j,histolog_rating,lvsi_rating] += 1

	
   	kappas[pathologist] = cohens_kappa(contingency_table[j,:,:].squeeze()).kappa_max

print np.median(contingency_table,axis=0)
print 0.5*(np.percentile(contingency_table,75,axis=0) - np.percentile(contingency_table,25,axis=0))
json.dump(kappas,open('lvsi-by-grade.json','wb'))
ap(np.median(kappas.values()))
print 0.5*(np.percentile(kappas.values(),75)-np.percentile(kappas.values(),25))