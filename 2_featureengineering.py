import pandas as pd 
import numpy as np
from  aiqutils.data_preparation import interact_categorical_numerical

import importlib


df = pd.read_csv('output/partidos_equipo.csv')

df =  df.drop_duplicates()



df["fecha"] = pd.to_datetime(df.fecha, format = "%Y-%m-%d")
df["MONTH"] = df.fecha.apply(lambda x:  x.month)
df["YEAR"] = df.fecha.apply(lambda x:  x.year)


date_col = "fecha"
fillmethod = "zeros"

lag_col          = "partido_equipo_num"
numerical_cols   = ["estadio_asistencia", 'dias_ultimopartido', 'goles_anotados']
categorical_cols = ["equipo"]
lag_list         = [1]
rolling_list     = [1, 3, 6, 12, 24]



#df_ewm = interact_categorical_numerical(
#                                   df, lag_col, numerical_cols,
#                                   categorical_cols, lag_list,
#                                   rolling_list, agg_funct="sum",
#                                   rolling_function = "ewm", freq=None,
#                                   group_name=None, store_name=False)
df_rolling = interact_categorical_numerical(
                                   df, lag_col, numerical_cols,
                                   categorical_cols, lag_list,
                                   rolling_list, agg_funct="sum",
                                   rolling_function = "rolling", freq=None,
                                   group_name=None, store_name=False)
#df_expansion = interact_categorical_numerical(
#                                   df, lag_col, numerical_cols,
#                                   categorical_cols, lag_list,
#                                   rolling_list, agg_funct="sum",
#                                   rolling_function = "expanding", freq=None,
#                                   group_name=None, store_name=False)


id_columns = ['equipo', "partido_equipo_num"]
#df= df.merge(df_ewm, on = id_columns )
#df= df.merge(df_expansion, on = id_columns )
#df = df[['equipo', 'fecha', "partido_equipo_num", 'estadio_asistencia']]
df= df.merge(df_rolling, on = id_columns )
df = df.sort_values(['equipo','fecha'])


cuantiles_4_asistencia  = pd.qcut(df.groupby('equipo')['estadio_asistencia'].mean(), 4, labels=False).to_dict()
cuantiles_6_asistencia  = pd.qcut(df.groupby('equipo')['estadio_asistencia'].mean(), 6, labels=False).to_dict()
cuantiles_10_asistencia  = pd.qcut(df.groupby('equipo')['estadio_asistencia'].mean(), 10, labels=False).to_dict()

df['quantile_4_asistencia'] = df.equipo.map(cuantiles_4_asistencia)
df['quantile_6_asistencia'] = df.equipo.map(cuantiles_6_asistencia)
df['quantile_10_asistencia'] = df.equipo.map(cuantiles_10_asistencia)

cuantiles_4_pctocupacion  = pd.qcut(df.groupby('equipo')['estadio_ocupacion_pct'].mean(), 4, labels=False).to_dict()
cuantiles_6_pctocupacion  = pd.qcut(df.groupby('equipo')['estadio_ocupacion_pct'].mean(), 6, labels=False).to_dict()
cuantiles_10_pctocupacion  = pd.qcut(df.groupby('equipo')['estadio_ocupacion_pct'].mean(), 10, labels=False).to_dict()

df['quantile_4_pctocupacion'] = df.equipo.map(cuantiles_4_pctocupacion)
df['quantile_6_pctocupacion'] = df.equipo.map(cuantiles_6_pctocupacion)
df['quantile_10_pctocupacion'] = df.equipo.map(cuantiles_10_pctocupacion)

hue_order =  ['Atlante', 'Puebla F.C.', 'Club Atlético de San Luis', 'Lobos BUAP',
       'Monarcas Morelia', 'Atlas', 'Universidad de Guadalajara',
       'Universidad Nacional', 'Gallos Blancos de Querétaro',
       'Jaguares de Chiapas', 'Toluca', 'Tiburones Rojos de Veracruz',
       'América', 'Necaxa', 'Cruz Azul', 'Santos Laguna', 'FC Juárez', 'León',
       'Pachuca', 'Dorados de Sinaloa', 'Guadalajara', 'Club Tijuana',
       'Rayados de Monterrey', 'Tigres de la U.A.N.L.']

df.to_csv('output/partidos_equipos_featuregenerated.csv', index = False)
