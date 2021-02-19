import pandas as pd
import logging 
import numpy as np 
#%matplotlib 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.ERROR)
logging.debug('start program')

path = "Asistencia BBVA V2.xls"
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
    df_distance = df_sheet
    logging.info('Distance File procesed...' +sheet)

  else:
    logging.error('sheet not recognized...', sheet)



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
#TODO: DELETE
'ENFRENTAMIENTO':'enfrentamiento', #? 557 unique values each team has played 4.314(x2) times with each other team on average.
#TODO: Repeat this column using local and visitors columns to avoid typos
#TODO: Plot of distribution of matches, which matches repeat the most
'FECHA':'fecha',
#TODO: Convert to date format
'Día de la semana':'dia_semana',
##TODO: delete acentos
'¿Es fín de semana?':'findesemana',
#TODO: make boolean
'HORA POR BLOQUE':'hora_bloque', #? tehre are 17 unique values, matches start at 12pm until 23pm. There are 22 values taht start at fraction hours
#TODO: should we delete the 22 extra values or are these special values that indicate special matches?
'HORA DEL PARTIDO':'hora_partido', #? 55 unique values, 54 missing values. Most matches start at XX:00 XX:30 and XX:45 hours
#TODO: We could move the atypical starting hours to XX:00 XX:30 and XX:45  and create a boolan for starting_special for special cases
'LOCAL':'equipo_local', #? 29 total teams, names matches in both equipo_local, equipo_visitante
'VISITANTE':'equipo_visitante', 
'ESTADIO':'estadio', #? 35 different stadiums.
#TODO: Some values look repeated, in particular  
#TODO'Universitario', 'Universitario BUAP' -  
#TODO'OLIMPICO BENITO JUAREZ' 'Olímpico Benito Juárez' 'Olímpico Universitario', -  
#TODO 'La Corregidora' 'La Corregidora / UNAM' -  
#TODO 'Jalisco' 'Jalisco / U de G', - 
#TODO 'Estadio BBVA', 'Estadio BBVA Bancomer', -
#TODO 'Estadio AKRON','Estadio AKRON - Omnilife / Chivas',
#TODO 'Cuauhtémoc', 'Cuauhtémoc / Jaguares',
#TODO  'Azteca' 'Azteca / Cruz Azul',
#TODO: Pregunta: Why some names have a slash symbol on the name, what does the slash stands for...
'AFORO':'aforo', #? Mean: 38,792 Max: 100,248 Min:12,000
'ASISTENCIA':'asistencia',
#TODO: Replace some strings in the file to create a numeric columsn [" "]
'Goles anotados':'goles_anotados', #? mean: 2.63 
'%DE OCUPACIÓN':'estadio_ocupacion_pct', #? mean: 65% std: 24%  (40-80%)
#TODO: Delete na
'PARTIDO ASISTENCIA':'estadio_asistencia', #? string ocupacion we can delete this feature
'¿El Local pertenece a los 4 Grandes?':'cuatrograndes_local', #? 4 grandes == 'América', 'Universidad Nacional', 'Guadalajara', 'Cruz Azul'
#TODO: Convert to boolena df_matches.cuatrograndes_local.apply(lambda x: True if x =='sí' else False)
'ENF':'enf',
#TODO: Delete column
'¿El Visitante pertenece a los 4 Grandes?':'cuatrograndes_visitante',
'Distancia entre el Equipo Visitante y el Equipo Local':'distancia_equipos', #? There are three blocks 0-1000 1000-3000 3000+
#TODO: We still need to fill some empty values for 27 rows
'Tipo de Clasico':'tipo_clasico'}  
#?  clasico types = {'Clásico Nacional':'América vs Guadalajara',
#? 'Clásico del Centro':'Club Atlético de San Luis vs Gallos Blancos de Querétaro',
#? 'Clásico Capitalino': 'Universidad Nacional vs América',
#? 'Clásico Tapatío':'Guadalajara vs Atlas', 
#?'Clásico Regio': 'Rayados de Monterrey vs Tigres de la U.A.N.L.']


df_matches = df_matches.rename(columns=rename_columns)
      