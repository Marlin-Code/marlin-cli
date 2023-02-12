import requests
import constants

def get_module(module_name):
    module = None
    error = None
    response = requests.get(url=f"{constants.API_URL}/modules/{module_name}")
    if response.ok:
        module = response.json()
    else:
        error = {"code": response.status_code, "message": response.content}
    return (module, error)

def list_modules():
    module_list = None
    error = None
    response = requests.get(url=f"{constants.API_URL}/modules")
    if response.ok:
        module_list = response.json()
    else:
        error = {"code": response.status_code, "message": response.content}
    return (module_list, error)
