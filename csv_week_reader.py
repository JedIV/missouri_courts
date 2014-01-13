from pandas import *

evictions = read_csv("region_six_list.csv")

evictions.columns = ['rank','caseID','case_type','date','location','case_style']

for index, row in evictions.iterrows():
    print row['caseID']
