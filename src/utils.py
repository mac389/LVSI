import json,itertools

import numpy as np 
import pandas as pd 

from statsmodels.stats.inter_rater import cohens_kappa

def kappa(f1,f2,pathologists,cols_to_parse,outname,ratings):
	contingency_tables = {}
	lvsi = {}
	for (pathologist_one, pathologist_two) in itertools.combinations(pathologists,2):

		KEY = '%s-%s'%(pathologist_one,pathologist_two)

		df_one = pd.read_excel(f1,pathologist_one,parse_cols=cols_to_parse, convert_float=True)
		df_two = pd.read_excel(f2,pathologist_two,parse_cols=cols_to_parse, convert_float=True)

		patho_one_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in df_one.apply(np.nonzero,axis=1).values]).astype(int)
		patho_two_ratings = np.array([i[0][0] if len(i[0]) > 0 else -1 for i in df_two.apply(np.nonzero,axis=1).values]).astype(int)

		#-1 indicates an invalid value in case the rater forgot to fill the form out
		table = [[np.logical_and(patho_one_ratings == rating_one,patho_two_ratings == rating_two).sum()
								for rating_one in ratings] 
								for rating_two in ratings]
		
		contingency_tables[KEY] = table
		lvsi['%s-%s'%(pathologist_one,pathologist_two)] = cohens_kappa(table).kappa

	json.dump(lvsi,open('../data/%s.json'%outname,'wb'))
	return contingency_tables
