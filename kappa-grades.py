import itertools, json

import pandas as pd
import numpy as np 
from awesome_print import ap 
from statsmodels.stats.inter_rater import cohens_kappa, to_table

possible_grades = ['1','2','3']
cols_with_grades = [4,5,6]
pathologists = open('rater-names','rb').read().splitlines()

kappas = {}
for (pathologist_one, pathologist_two) in itertools.combinations(pathologists,2):

	df_one = pd.read_excel('no-stain.xls',pathologist_one,parse_cols=cols_with_grades, convert_float=False)
	df_two = pd.read_excel('no-stain.xls',pathologist_two,parse_cols=cols_with_grades, convert_float=False)

	patho_one_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in df_one.apply(np.nonzero,axis=1).values]).astype(int)
	patho_two_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in df_two.apply(np.nonzero,axis=1).values]).astype(int)

	contingency_table = pd.crosstab(patho_one_ratings,patho_two_ratings)
	if contingency_table.shape[0]>3:
		contingency_table = contingency_table.values[1:,1:]
	else:
		contingency_table = contingency_table.values

	kappas['%s-%s'%(pathologist_one,pathologist_two)] = cohens_kappa(contingency_table).kappa_max

#json.dump(kappas,open('kappa-grades.json','wb'))

ap(np.median(kappas.values()))
print 0.5*(np.percentile(kappas.values(),75)-np.percentile(kappas.values(),25))