import itertools, json

import pandas as pd
import numpy as np 
from awesome_print import ap 
from statsmodels.stats.inter_rater import cohens_kappa, to_table

possible_grades = ['1','2','3']
cols_with_grades = [1,2,3]
pathologists = open('../data/rater-names','rb').read().splitlines()

lvsi = {}
for (pathologist_one, pathologist_two) in itertools.combinations(pathologists,2):

	df_one = pd.read_excel('../data/stains.xls',pathologist_one,parse_cols=cols_with_grades, convert_float=False)
	df_two = pd.read_excel('../data/stains.xls',pathologist_two,parse_cols=cols_with_grades, convert_float=False)

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


	lvsi['%s-%s'%(pathologist_one,pathologist_two)] = cohens_kappa(contingency_table).kappa

json.dump(lvsi,open('../data/lvsi-stains-grades.json','wb'))

ap(np.median(lvsi.values()))
print 0.5*(np.percentile(lvsi.values(),75)-np.percentile(lvsi.values(),25))