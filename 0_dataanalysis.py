import pandas as pd
import logging 
import numpy as np
import datetime 
import pdb 
from sklearn import linear_model
from utils import round_hours, create_unique_enfrentamiento, read_distance_file, missingnumeric_regression_autocomplete
from openpyxl import load_workbook
#%matplotlib 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.ERROR)
logging.debug('start program')

path = "Asistencia BBVA V2.xlsx"
excel = pd.read_excel(path)
xls = pd.ExcelFile(path)
sheets = xls.sheet_names

files_dict = dict()
df_matches = pd.DataFrame()
df_distance = pd.DataFrame()

for sheet in sheets:
  df_sheet = pd.read_excel(path, sheet_name=sheet)
  df_sheet['sheetname'] = sheet

  if "BBVA" in sheet:
    df_matches = df_matches.append(df_sheet)
    logging.info('Match File procesed...'+ sheet)
  elif "Distancia" in sheet:
    df_distance = read_distance_file( path, sheet, 'D3', 'AB27')
    logging.info('Distance File procesed...' +sheet)

  else:
    logging.error('sheet not recognized...' +sheet)



for col in df_matches.columns:
  print("\n\n---------------------" + col +"--------------")
  print(df_matches[col].describe())
  print('Col na %: ' + str(np.sum(df_matches[col].isna())/len(df_matches)))

rename_columns = {'TORNEO':'torneo', #? 16 unique torneos
'TORNEO NO':'torneo_num', #? 16 torneos in ascending order from 1 tyo 16
'JORNADA':'jornada', #? 19 jornadas in ascending orrder from JORNADA 1 to JORNADA 18
#TODO: Pregunta: Why there are more jornadas than torneos
'TIPO JORNADA':'jornada_tipo', #? Two unique values: FIN DE SEMANA, DOBLE
#TODO: Pregunta: What is DOBLE? Two teams playing at teh same time?
'FASE':'fase', #? Only one value 
#TODO: Pregunta: Why do we only have one value
'NO PARTIDO':'partido_num', #? Two entries per partido_num (one for visitors and one for locals) 2403 total matches
'DÍA':'dia', #? Day of the week from monday to Sunday
#* TODO DELETE
'ENFRENTAMIENTO':'enfrentamiento', #? 557 unique values each team has played 4.314(x2) times with each other team on average.
#* TODO Repeat this column using local and visitors columns to avoid typos
#TODO Plot of distribution of matches, which matches repeat the most
#* TODO Complete test for create_unique_enfrentamiento
'FECHA':'fecha',
#* TODO Convert to date format
'Día de la semana':'dia_semana',
#* TODO delete acentos
'¿Es fín de semana?':'findesemana',
#* TODO make boolean
'HORA POR BLOQUE':'hora_bloque', #? tehre are 17 unique values, matches start at 12pm until 23pm. There are 22 values taht start at fraction hours
#TODO should we delete the 22 extra values or are these special values that indicate special matches?
#* TODO Fucntion round_hours implemented
'HORA DEL PARTIDO':'hora_partido', #? 55 unique values, 54 missing values. Most matches start at XX:00 XX:30 and XX:45 hours
#TODO PREGUNTA: We could move the atypical starting hours to XX:00 XX:30 and XX:45  and create a boolan for starting_special for special cases
#* TODO Fucntion round_hours implemented
'LOCAL':'equipo_local', #? 29 total teams, names matches in both equipo_local, equipo_visitante
'VISITANTE':'equipo_visitante', 
'ESTADIO':'estadio', #? 35 different stadiums.
#TODO Some values look repeated, in particular  
#TODO'Universitario', 'Universitario BUAP' -  
#TODO'OLIMPICO BENITO JUAREZ' 'Olímpico Benito Juárez' 'Olímpico Universitario', -  
#TODO 'La Corregidora' 'La Corregidora / UNAM' -  
#TODO 'Jalisco' 'Jalisco / U de G', - 
#TODO 'Estadio BBVA', 'Estadio BBVA Bancomer', -
#TODO 'Estadio AKRON','Estadio AKRON - Omnilife / Chivas',
#TODO 'Cuauhtémoc', 'Cuauhtémoc / Jaguares',
#TODO 'Azteca' 'Azteca / Cruz Azul',
#TODO  Pregunta: Why some names have a slash symbol on the name, what does the slash stands for...
'AFORO':'aforo', #? Mean: 38,792 Max: 100,248 Min:12,000
'ASISTENCIA':'estadio_asistencia',
#* TODO  Replace some strings in the file to create a numeric columsn [" "]
'Goles anotados':'goles_anotados', #? mean: 2.63 
'%DE OCUPACIÓN':'estadio_ocupacion_pct', #? mean: 65% std: 24%  (40-80%)
#* TODO Delete na recreated entire column using aforo/estadio_ocupacion
'PARTIDO ASISTENCIA':'partido_asistencia', #? string ocupacion we can delete this feature
'¿El Local pertenece a los 4 Grandes?':'cuatrograndes_local', #? 4 grandes == 'América', 'Universidad Nacional', 'Guadalajara', 'Cruz Azul'
#* TODO Convert to boolena df_matches.cuatrograndes_local.apply(lambda x: True if x =='sí' else False)
'ENF':'enf',
# * TODO Delete column
'¿El Visitante pertenece a los 4 Grandes?':'cuatrograndes_visitante',
#* TODO Convert to boolean 
'Distancia entre el Equipo Visitante y el Equipo Local':'distancia_equipos', #? There are three blocks 0-1000 1000-3000 3000+
#TODO We still need to fill some empty values for 27 rows
'Tipo de Clasico':'tipo_clasico'}  
#?  clasico types = {'Clásico Nacional':'América vs Guadalajara',
#? 'Clásico del Centro':'Club Atlético de San Luis vs Gallos Blancos de Querétaro',
#? 'Clásico Capitalino': 'Universidad Nacional vs América',
#? 'Clásico Tapatío':'Guadalajara vs Atlas', 
#?'Clásico Regio': 'Rayados de Monterrey vs Tigres de la U.A.N.L.']

df_matches = df_matches.rename(columns=rename_columns)

delete_columns = ['partido_asistencia', 'enf']
for col in delete_columns:
  del df_matches[col]

team_list= df_matches.equipo_local.unique() 
df_matches = create_unique_enfrentamiento(df_matches, team_list)
#convert to date format
df_matches['fecha'] = pd.to_datetime(df_matches.fecha)
#conver dia_semana
map_dia_semana = {'Fri': 'viernes', 
                  'Sat':'sabado', 
                  'Sun':'domingo', 
                  'Tue':'martes', 
                  'Wed':'miercoles',
                  'Thu':'jueves', 
                  'Mon':'lunes'}
df_matches['dia_semana'] = df_matches.dia_semana.map(map_dia_semana)

#findesemana covert to boolean
map_findesemana = {'sí':True, 'no':False}
df_matches["findesemana"] = df_matches.findesemana.map(map_findesemana)


#Create round variables to create fewer variables in time block variables
df_matches =  round_hours(df_matches, "hora_bloque")
# TODO Icnomplete data use regression df =  round_hours(df_matches, "hora_partido")

df_matches.reset_index(inplace = True)
del df_matches['index']

for col in df_matches.columns:
  if np.sum(df_matches[col].isna()) >0:
    print(col)

#Replace empty values in estadio_asistencia
df_matches['estadio_asistencia'] =pd.to_numeric(df_matches.estadio_asistencia, errors='coerce') #TODO Replace asistencia -> estadio_asistencia
df_matches = missingnumeric_regression_autocomplete(df_matches, 'estadio_asistencia')
#df_matches = missingnumeric_regression_autocomplete(df_matches, 'aforo')
#df_matches = missingnumeric_regression_autocomplete(df_matches, 'estadio_asistencia')
#Recreate estadio_ocupacion_pct
df_matches['estadio_ocupacion_pct'] =  df_matches.estadio_asistencia/ df_matches.aforo
#Convert cuatro_grandes to boolean
df_matches['cuatrograndes_local']= df_matches.cuatrograndes_local.apply(lambda x: True if x =='sí' else False)
df_matches['cuatrograndes_visitante']= df_matches.cuatrograndes_visitante.apply(lambda x: True if x =='sí' else False)

df_matches.to_csv('output/bbva_matches.csv') 


