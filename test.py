import pandas as pd 
import numpy as np 
import datetime 
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

df_resultados = pd.read_csv('input/resultados_partidos.csv')
map_columns = { 'Season':'temporada', 
 'Date':'fecha', 
 'Time':'hora', 
 'Home':'equipo_local', 
 'Away':'equipo_visitante', 
'HG':'equipo_local_goles',
'AG':'equipo_visitante_goles', 
'Res':'equipo_ganador'}

df_resultados = df_resultados[map_columns.keys()]
df_resultados = df_resultados.rename(columns=map_columns)
print(df_resultados.head())
df_resultados['fecha_hora'] = pd.to_datetime(df_resultados['fecha']+ ' ' +df_resultados['hora'])
df_resultados['fecha_hora_mexico'] = df_resultados['fecha_hora'].dt.tz_localize('UTC').dt.tz_convert('America/Mexico_City')


df_resultados['fecha_mexico'] =  pd.to_datetime(df_resultados['fecha_hora_mexico'].apply(lambda x: x.date())) 

df_resultados['fecha'] = pd.to_datetime(df_resultados.fecha)


df_ocupacion = pd.read_csv('output/bbva_matches.csv')
df_ocupacion['fecha_mexico'] = pd.to_datetime(df_ocupacion.fecha)
df_ocupacion['fecha_hora'] = pd.to_datetime(df_ocupacion['fecha']+ ' ' +df_ocupacion['hora_partido'])


map_equipos = { 
       'Chiapas': 'Jaguares de Chiapas',
       'Queretaro': 'Gallos Blancos de Querétaro',
       'Monterrey':'Rayados de Monterrey',
       'Monarcas': 'Monarcas Morelia', 
       'Club Leon': 'León', 
       'Club America':'América', 
       'Atl. San Luis': 'Club Atlético de San Luis', 
        'U.A.N.L.- Tigres': 'Tigres de la U.A.N.L.',
       'U.N.A.M.- Pumas':'Universidad Nacional',
       'Puebla': 'Puebla F.C.', 
       'Guadalajara Chivas': 'Guadalajara',
       'Veracruz':'Tiburones Rojos de Veracruz', 
       'Juarez' :'FC Juárez'
      }

#! There could be an error in the database as Universidad de Guadalajara doesn't appear
#! It could have been merge with Guadalajara Chivas ()
#TODO We will discover in the merge if something happened to the Guadalajara Universidad Team
df_resultados['equipo_local'] = df_resultados['equipo_local'].replace(map_equipos)
df_resultados['equipo_visitante'] = df_resultados['equipo_visitante'].replace(map_equipos)
      
def compare_teams(df_resultados, df_ocupacion):  
  equipos_resultados = df_resultados.equipo_local.unique()
  equipos_ocupacion = df_ocupacion.equipo_local.unique()

  for club_ocupacion in equipos_ocupacion:
    for club_result in equipos_resultados:
      if similar(club_ocupacion, club_result) > .5:
        print("Similar names: {} {} ".format(club_ocupacion, club_result)) 


test = df_resultados.merge(df_ocupacion, on = ['fecha_mexico', 'equipo_local', 'equipo_visitante'], how='outer', indicator=True)

test_right = test[test._merge == 'right_only']

rightonly_index = test_right[['fecha_mexico', 'equipo_local', 'equipo_visitante']]

test_left = test[test._merge == 'left_only']
test_both = test[test._merge == 'both']

