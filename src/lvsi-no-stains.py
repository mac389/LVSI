import utils as tech 

cols_with_grades = [1,2,3]
pathologists = open('../data/rater-names','rb').read().splitlines()

#No stains
f1 = '../data/no-stain.xls'
f2 = '../data/no-stain.xls'
tech.kappa(f1,f2,pathologists,cols_with_grades,'lvsi-grades')
