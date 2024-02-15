import pandas as pd

def get_all_company_info():
	
    #df_all=pd.concat([pd.read_csv(f) for f in tqdm(list(glob.glob('CINFO23/*.csv')))],axis=0)
	#df_all.to_csv('CINFO_NYSE_FEB2023.csv')
	df_all=pd.read_csv(r'C:\Users\compu\Downloads\CINFO_NYSE_FEB2023.csv')
	df_all.sector=df_all.sector.replace('Financial','Financial Services').replace('Industrial Goods','Industrials')
	return df_all