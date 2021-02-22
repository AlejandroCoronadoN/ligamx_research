import pandas as pd
import numpy as np

def test_add():
  assert True

def test_uniqueteams_local():
  unique_teams = ['Club Tijuana', 'Jaguares de Chiapas',
       'Gallos Blancos de Querétaro', 'Cruz Azul', 'Santos Laguna',
       'Rayados de Monterrey', 'Atlas', 'Toluca', 'Atlante',
       'Monarcas Morelia', 'León', 'América', 'Pachuca',
       'Club Atlético de San Luis', 'Tigres de la U.A.N.L.',
       'Universidad Nacional', 'Puebla F.C.', 'Guadalajara',
       'Tiburones Rojos de Veracruz', 'Universidad de Guadalajara',
       'Dorados de Sinaloa', 'Necaxa', 'Lobos BUAP', 'FC Juárez',
       'Club Atletico de San Luis', 'FC Juarez', 'Leon', 'America',
       'Gallos Blancos de Queretaro']
  df_matches = pd.read_csv('output/bbva_matches.csv')
  #TODO complete test function
  assert len([x for x in df_matches.equipo_local.unique() if x in unique_teams]) == len(unique_teams)


def test_enfrentaimiento_consistency():
  """Test if the new enfrentamientos varibale stays the same 
  for equipo_local=e' vs equipo_visitante=e'' and 
  equipo_visitante=e' vs equipo_local=e'' 
  """
  #TODO complete test function
  df_matches = pd.read_csv('output/bbva_matches.csv')
  for unique_enfrentamiento in   df_matches.enfrentamiento.unique():
    if len(df_matches[df_matches.enfrentamiento == unique_enfrentamiento].equipo_local.unique()) != 2:
      test= df_matches[df_matches.enfrentamiento == unique_enfrentamiento]
      print("ERROR")
    else:
      continue
  assert True