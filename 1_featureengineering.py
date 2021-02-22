import pandas as pd 
import numpy as np
from  aiqutils.data_preparation import interact_categorical_numerical

import importlib


df = pd.read_csv('/home/alejandro/Dropbox/Github/TenderFlakes/Weekly/data_regresion_brand_substitution.csv')
df = df.reset_index()

df =  df.drop_duplicates()
df["DESCRIPTION"] = df.DESCRIPTION.apply(lambda x:"producto_" + str(x))
df["MARKET_MEANING"] = df.MARKET_MEANING.apply(lambda x:"agencia_" + str(x))

df["DATE"] = pd.to_datetime(df.DATE, format = "%Y-%m-%d")
df["MONTH"] = df.DATE.apply(lambda x:  x.month)
df["YEAR"] = df.DATE.apply(lambda x:  x.year)

df = df.drop(['Unnamed: 0', 'BRAND', "index",
   'CATEGORY_SUBGROUP', 'CB_PRODUCT_SEGMENT', 'DAY',
   'MANUFACTURER', 'MARKET', 'MARKET_LEVEL', 'UPC',
   '_Vol', 'HOLIDAY_DUMMY',
   'RETAILER', 'COMPLIMENTS', 'SELECTION', 'TENDERFLAKE', 'WESTERN_FAMILY'], axis =1 )



date_col = "DATE"
id_columns = ['DESCRIPTION', 'MARKET_MEANING']
fillmethod = "zeros"


#df_test = aiqutils.data_preparation.fill_timeseries(df, id_columns, date_col, freq = "D", fillmethod = "zeros")
df["Avg_Retail_Unit_Price"] = (df.Avg_Retail_Unit_Price - df.Avg_Retail_Unit_Price.mean())/df.Avg_Retail_Unit_Price.std()

lag_col          = "DATE"
numerical_cols   = ["Avg_Retail_Unit_Price"]
categorical_cols = ["MARKET_MEANING", "DESCRIPTION"]
lag_list         = [1,2,3,4,6,8,10,12,16]
rolling_list     = [1,2,3,4,6,8,12,16,20]



df_ewm = interact_categorical_numerical(
                                   df, lag_col, numerical_cols,
                                   categorical_cols, lag_list,
                                   rolling_list, agg_funct="sum",
                                   rolling_function = "ewm", freq=None,
                                   group_name=None, store_name=False)
df_rolling = interact_categorical_numerical(
                                   df, lag_col, numerical_cols,
                                   categorical_cols, lag_list,
                                   rolling_list, agg_funct="sum",
                                   rolling_function = "rolling", freq=None,
                                   group_name=None, store_name=False)
df_expansion = interact_categorical_numerical(
                                   df, lag_col, numerical_cols,
                                   categorical_cols, lag_list,
                                   rolling_list, agg_funct="sum",
                                   rolling_function = "expanding", freq=None,
                                   group_name=None, store_name=False)


id_columns = ['DESCRIPTION', 'MARKET_MEANING', "DATE"]
df= df.merge(df_ewm, on = id_columns )
df= df.merge(df_expansion, on = id_columns )
df= df.merge(df_rolling, on = id_columns )

