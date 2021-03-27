import pandas as pd
import logging 
import numpy as np
import datetime 
import pdb 
from sklearn import linear_model
from utils import round_hours, create_unique_enfrentamiento, read_distance_file, missingnumeric_regression_autocomplete
#from openpyxl import load_workbook
#%matplotlib 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.ERROR)
logging.debug('start program')

path = "input/Asistencia BBVA V2.xlsx"
excel = pd.read_excel(path)
xls = pd.ExcelFile(path)
sheets = xls.sheet_names

files_dict = dict()
df_ocupacion = pd.DataFrame()
df_distance = pd.DataFrame()

for sheet in sheets:
  df_sheet = pd.read_excel(path, sheet_name=sheet)
  #df_sheet['sheetname'] = sheet #<- Needed to due to duplicates
  
  if "BBVA" in sheet:
    df_ocupacion = df_ocupacion.append(df_sheet)
    logging.info('Match File procesed...'+ sheet)
  elif "Distancia" in sheet:
    df_distance = read_distance_file( path, sheet, 'D3', 'AB27')
    logging.info('Distance File procesed...' +sheet)

  else:
    logging.error('sheet not recognized...' +sheet)



for col in df_ocupacion.columns:
  print("\n\n---------------------" + col +"--------------")
  print(df_ocupacion[col].describe())
  print('Col na %: ' + str(np.sum(df_ocupacion[col].isna())/len(df_ocupacion)))

rename_columns = {'TORNEO':'torneo', #? 16 unique torneos
'TORNEO NO':'torneo_num', #? 16 torneos in ascending order from 1 tyo 16
'JORNADA':'jornada', #? 19 jornadas in ascending orrder from JORNADA 1 to JORNADA 18
#* TODO Pregunta: Why there are more jornadas than torneos
'TIPO JORNADA':'jornada_tipo', #? Two unique values: FIN DE SEMANA, DOBLE
#* TODO Pregunta: What is DOBLE? Two teams playing at teh same time? Special Reeschedules, two teams have to play at the same time same day
'FASE':'fase', #? Only one value 
#* TODO Pregunta: Why do we only have one value
'NO PARTIDO':'partido_num', #? Two entries per partido_num (one for visitors and one for locals) 2403 total matches
'DÍA':'dia', #? Day of the week from monday to Sunday
#* TODO DELETE
'ENFRENTAMIENTO':'enfrentamiento', #? 557 unique values each team has played 4.314(x2) times with each other team on average.
#* TODO Repeat this column using local and visitors columns to avoid typos
#* TODO Plot of distribution of matches, which matches repeat the most
#* TODO Complete test for create_unique_enfrentamiento
'FECHA':'fecha',
#* TODO Convert to date format
'Día de la semana':'dia_semana',https://colab.research.google.com/drive/1QbdXKvKlkwP_uGz-GT29mW2qEMu462kf?authuser=1#scrollTo=oi-2mZ7DrheF
'HORA POR BLOQUE':'hora_bloque', #? tehre are 17 unique values, matches start at 12pm until 23pm. There are 22 values taht start at fraction hours
#* TODO should we delete the 22 extra values or are these special values that indicate special matches?
#* TODO Fucntion round_hours implemented
'HORA DEL PARTIDO':'hora_partido', #? 55 unique values, 54 missing values. Most matches start at XX:00 XX:30 and XX:45 hours
#* TODO PREGUNTA: We could move the atypical starting hours to XX:00 XX:30 and XX:45  and create a boolan for starting_special for special cases
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
#* TODO Convert to boolena df_ocupacion.cuatrograndes_local.apply(lambda x: True if x =='sí' else False)
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

df_ocupacion = df_ocupacion.rename(columns=rename_columns)

delete_columns = ['partido_asistencia', 'enf', 'dia']
for col in delete_columns:
  del df_ocupacion[col]

team_list= df_ocupacion.equipo_local.unique() 
df_ocupacion = create_unique_enfrentamiento(df_ocupacion, team_list)
#convert to date format
df_ocupacion['fecha'] = pd.to_datetime(df_ocupacion.fecha)
#conver dia_semana
map_dia_semana = {'Fri': 'viernes', 
                  'Sat':'sabado', 
                  'Sun':'domingo', 
                  'Tue':'martes', 
                  'Wed':'miercoles',
                  'Thu':'jueves', 
                  'Mon':'lunes'}
df_ocupacion['dia_semana'] = df_ocupacion.dia_semana.map(map_dia_semana)

#findesemana covert to boolean
map_findesemana = {'sí':True, 'no':False}
df_ocupacion["findesemana"] = df_ocupacion.findesemana.map(map_findesemana)


#Create round variables to create fewer variables in time block variables
df_ocupacion =  round_hours(df_ocupacion, "hora_bloque")
# TODO Icnomplete data use regression df =  round_hours(df_ocupacion, "hora_partido")

df_ocupacion.reset_index(inplace = True)
del df_ocupacion['index']

for col in df_ocupacion.columns:
  if np.sum(df_ocupacion[col].isna()) >0:
    print(col)

#Replace empty values in estadio_asistencia
df_ocupacion['estadio_asistencia'] =pd.to_numeric(df_ocupacion.estadio_asistencia, errors='coerce') #TODO Replace asistencia -> estadio_asistencia
df_ocupacion = missingnumeric_regression_autocomplete(df_ocupacion, 'estadio_asistencia')
#df_ocupacion = missingnumeric_regression_autocomplete(df_ocupacion, 'aforo')
#df_ocupacion = missingnumeric_regression_autocomplete(df_ocupacion, 'estadio_asistencia')
#Recreate estadio_ocupacion_pct
df_ocupacion['estadio_ocupacion_pct'] =  df_ocupacion.estadio_asistencia/ df_ocupacion.aforo
#Convert cuatro_grandes to boolean
cuatrograndes = ['América', 'Universidad Nacional', 'Guadalajara', 'Cruz Azul']
df_ocupacion['cuatrograndes_local']= df_ocupacion.equipo_local.apply(lambda x: True if  x in cuatrograndes else False)
df_ocupacion['cuatrograndes_visitante']=  df_ocupacion.equipo_visitante.apply(lambda x: True if  x in cuatrograndes else False)
#Use fixed values from enfrentamientos to find clasicos
clasico_map = {'América VS Cruz Azul': 'Clásico Joven' ,
  'Guadalajara VS América': 'Clásico Nacional' ,
  'Club Atlético de San Luis VS Gallos Blancos de Querétaro': 'Clásico del  Centro',
  'Universidad Nacional VS América' : 'Clásico Capitalino' ,
  'Guadalajara VS Atlas': 'Clásico Tapatío' ,
  'Tigres de la U.A.N.L. VS Rayados de Monterrey': 'Clásico Regio' }

df_ocupacion.tipo_clasico.apply(lambda x: 'No clásico' if x not in clasico_map.keys() else '')
df_ocupacion['tipo_clasico'] =  df_ocupacion['enfrentamiento'].map(clasico_map)


map_estadios = {'OLIMPICO BENITO JUAREZ': 'Olímpico Benito Juárez',  
'Olímpico Universitario':'Olímpico Universitario',
'La Corregidora / UNAM': 'La Corregidora',
'Jalisco / U de G': 'Jalisco',  
'Estadio BBVA Bancomer': 'Estadio BBVA',
'Estadio AKRON - Omnilife / Chivas': 'Estadio AKRON',
'Cuauhtémoc / Jaguares': 'Cuauhtémoc',
'Azteca / Cruz Azul':'Azteca' }


map_equipos = {'Gallos Blancos de Queretaro':'Gallos Blancos de Querétaro',
'America' :'América',
'Leon':'León',
'Club Atletico de San Luis':'Club Atlético de San Luis',
'FC Juarez':'FC Juárez'}

df_ocupacion['estadio'] =  df_ocupacion.estadio.replace(map_estadios)
df_ocupacion['equipo_local'] =  df_ocupacion.equipo_local.replace(map_equipos)
df_ocupacion['equipo_visitante'] =  df_ocupacion.equipo_visitante.replace(map_equipos)

distance_columns = ['equipo_local', 'equipo_visitante', 'distancia_equipos']
df_distances = df_ocupacion[distance_columns].groupby(distance_columns).first().reset_index()
del df_ocupacion['distancia_equipos']
df_ocupacion =df_ocupacion.merge(df_distances, on = ['equipo_local', 'equipo_visitante'], how='left')

df_ocupacion['month'] = df_ocupacion.fecha.apply(lambda x: x.month)
df_ocupacion['year'] = df_ocupacion.fecha.apply(lambda x: x.year)
df_ocupacion['day'] = 1
df_ocupacion['date_year_month'] = pd.to_datetime(df_ocupacion[['year', 'month', 'day']])

#Drop duplicates most duplicates are created because different sheets contain same information
df_ocupacion = df_ocupacion.drop_duplicates()
df_ocupacion.to_csv('output/ocupacion_nivelpartido.csv', index =False) 


