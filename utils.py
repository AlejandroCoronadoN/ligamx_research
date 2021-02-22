import pandas as pd
import logging 
import numpy as np
import datetime 

def create_unique_enfrentamiento(df, team_list):
  """This function is used to create a unique enfrentamiento tag for 
  all the possible combinations of equipo_visitante and equipo_local
  such that for e' in equipo_visitante and e'' in equipo_local
   efrentamiento(e',e'')== enfrentamiento(e'',e')

  Args:
      df (DataFrame): df_matchhes, BBVA dataset
      team_list ([string]): List with the name of all the teams
  """
  enfrentamiento_list =[]
  for e in team_list:
    for e_2 in team_list:
      if e == e_2:
        continue
      else:
        enfrentamiento_list.append(e + " VS " +e_2 )
  
  df['enfrentamiento'] = df['equipo_local'] + " VS " + df['equipo_visitante']
  for enfrentamiento in enfrentamiento_list:
    team1 = enfrentamiento.split(" VS ")[0]
    team2 = enfrentamiento.split(" VS ")[1]
    df.loc[df['enfrentamiento'].apply(lambda x: True if (team1 == x.split(" VS ")[0] or team1 == x.split(" VS ")[1]) and (team2 == x.split(" VS ")[0] or team2 == x.split(" VS ")[1]) else False), 'enfrentamiento'] = enfrentamiento

  return df

def round_hours(df, col):
  """This function uses datetime.time variables and round them to
  complete or half hours. In the context of the dataset there are only a couple
  of matches that start at fraction hours. We would like to condense the information
  in bigger blocks.

  Args:
      df ([DataFrame]): []
      col ([string]): Name of the column to perform operation
  #TODO Create test for parsing hours correctly, what if we don't get datetime.time variables?
  """
  map_blocks = {}
  time_blocks = df[col].unique()
  col_round = col + '_round'
  df[col_round] = df[col].copy()
  for block in time_blocks:
    #pdb.set_trace()
    if block.minute !=0 and block.minute != 30:
      if 30-block.minute  > 15: #round to 0:
        newblock = datetime.time(block.hour, 0)
      else: #round to 30
        newblock = datetime.time(block.hour, 30)
      df.loc[df[col]==block, col_round] = newblock
  
  return df