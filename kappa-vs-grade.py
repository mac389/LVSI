import itertools, json

import pandas as pd
import numpy as np 
from awesome_print import ap 
from statsmodels.stats.inter_rater import cohens_kappa, to_table

possible_grades = ['1','2','3']
cols_with_grades = [4,5,6]
pathologists = open('rater-names','rb').read().splitlines()

kappas = {}
contingency_table = np.zeros((len(pathologists)*(len(pathologists)-1)/2,3,3)).astype(int)

for j,(pathologist_one,pathologist_two) in enumerate(list(itertools.combinations(pathologists,2))):

	df_pathologist_one = pd.read_excel('stains.xls',pathologist_one,parse_cols=cols_with_grades,convert_float=False)
	df_pathologist_two = pd.read_excel('stains.xls',pathologist_two,parse_cols=cols_with_grades,convert_float=False)

	patho_one_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in df_pathologist_one.apply(np.nonzero,axis=1).values]).astype(int)
	patho_two_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in df_pathologist_two.apply(np.nonzero,axis=1).values]).astype(int)

	for rating_one,rating_two in zip(patho_one_ratings,patho_two_ratings):
		#print rating_one,rating_two
		if type(rating_one) == type(list):
			rating_one = rating_one[0]
		if type(rating_two) == type(list):
			rating_two = rating_two[0]
		#print i 
		contingency_table[j,rating_one,rating_two] += 1

	
   	kappas['%s-%s'%(pathologist_one,pathologist_two)] = cohens_kappa(contingency_table[j,:,:].squeeze()).kappa_max

print np.median(contingency_table,axis=0)
print 0.5*(np.percentile(contingency_table,75,axis=0) - np.percentile(contingency_table,25,axis=0))
json.dump(kappas,open('kappa-by-grade-no-ihc.json','wb'))
ap(np.median(kappas.values()))
print 0.5*(np.percentile(kappas.values(),75)-np.percentile(kappas.values(),25))

'''	
	df_one = pd.read_excel('stains.xls',pathologist,parse_cols=cols_with_grades, convert_float=False)
	df_two = pd.read_excel('no-stain.xls',pathologist,parse_cols=cols_with_grades, convert_float=False)

	patho_one_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in df_one.apply(np.nonzero,axis=1).values]).astype(int)
	patho_two_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in df_two.apply(np.nonzero,axis=1).values]).astype(int)

	#Really inefficient implementation, but too many exceptions to vectorize:

	contingency_table = np.zeros((3,3))

	for rating_one in patho_one_ratings:
		if type(rating_one) == type(list):
			rating_one = rating_one[0]
		for rating_two in patho_two_ratings:
			if type(rating_two) == type(list):
				rating_two = rating_two[0]
			print '\t %d'%rating_two
			contingency_table[rating_one,rating_two] += 1


	lvsi[pathologist] = cohens_kappa(contingency_table).kappa_max

json.dump(lvsi,open('intra-rater-reliability.json','wb'))

ap(np.median(lvsi.values()))
print 0.5*(np.percentile(lvsi.values(),75)-np.percentile(lvsi.values(),25))
'''