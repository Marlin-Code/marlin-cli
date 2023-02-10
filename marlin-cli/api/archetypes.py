import requests
import constants


def get_archetype(archetype_name):
    archetype = None
    error = None
    response = requests.get(url=f"{constants.API_URL}/archetypes/{archetype_name}")
    if response.ok:
        archetype = response.json()
    else:
        error = {"code": response.status_code, "message": response.content}
    return (archetype, error)
