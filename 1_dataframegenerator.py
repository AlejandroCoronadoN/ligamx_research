import pandas as pd 
import numpy as np
from  aiqutils.data_preparation import interact_categorical_numerical
import importlib

df = pd.read_csv('output/bbva_matches.csv')
df =  df.drop_duplicates()
df['fecha'] = pd.to_datetime(df.fecha)
df_team_all = pd.DataFrame()

for col in df.columns:
  if np.sum(df[col].isna())>0:
    print('Deleeted Column: ' + col)
    del df[col]
    #TODO create functions to fix hora_partido distancia_equipos 

def is_cuatrograndes(df):
  cuatrograndes_list = ['América', 'Universidad Nacional', 'Guadalajara', 'Cruz Azul']
  if df.equipo.unique()[0] in cuatrograndes_list:
    df['cuatro_grandes'] =True
  else:
    df['cuatro_grandes'] =False  
  return df

for team in df.equipo_local.unique():
  df_team= df.loc[(df.equipo_local == team) | (df.equipo_visitante==team),]
  df_team['equipo'] =  team
  df_team = df_team.sort_values('fecha')
  df_team = df_team.reset_index()
  df_team['partido_equipo_num'] = df_team.index
  df_team['fecha_ultimopartido']= df_team.groupby(['equipo', 'partido_equipo_num']).first().shift(1)['fecha'].values
  df_team['dias_ultimopartido'] = df_team['fecha'] - df_team['fecha_ultimopartido']
  df_team = df_team.dropna()
  df_team['dias_ultimopartido'] = df_team.dias_ultimopartido.apply(lambda x: x.days)
  df_team = is_cuatrograndes(df_team)
  df_team_all = df_team_all.append(df_team)

df_team_all.to_csv('output/partidos_equipo.csv')