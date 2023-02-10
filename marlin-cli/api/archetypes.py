import requests
import constants 

def get_archetype(archetype_name):
  response = requests.get(
    url=f"{constants.API_URL}/archetypes/{archetype_name}"
  )
  return response.json()