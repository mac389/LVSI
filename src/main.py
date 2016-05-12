import json

import utils as tech 
import numpy as np 

cols_with_grades = [1,2,3]
pathologists = open('../data/rater-names','rb').read().splitlines()

contingency_tables = {}

possible_values = list(np.array(cols_with_grades)-1)
#No stains
f1 = '../data/no-stain.xls'
f2 = '../data/no-stain.xls'
contingency_tables['no-stain'] = tech.kappa(f1,f2,pathologists,cols_with_grades,'lvsi-grades-s-stains',possible_values)

#Stains
f1 = '../data/stains.xls'
f2 = '../data/stains.xls'
contingency_tables['stain'] = tech.kappa(f1,f2,pathologists,cols_with_grades,'lvsi-grades-c-stains',possible_values)

#Intra-rater relaibility
#Stains
f1 = '../data/stains.xls'
f2 = '../data/no-stain.xls'
contingency_tables['Intra-rater']  = tech.kappa(f1,f2,pathologists,cols_with_grades,'intra-rater-reliability',possible_values)

json.dump(contingency_tables,open('../data/contingency_tables.json','wb'))