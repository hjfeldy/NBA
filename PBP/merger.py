import pandas as pd
import os

master = pd.DataFrame()

for i in range(1,27):
	
	df = pd.read_csv(f'pbp_raw{i}.csv')
	master = master.append(df) 

master.to_csv('master.csv')
