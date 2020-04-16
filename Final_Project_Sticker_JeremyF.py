# Jeremy Fisher 4/15/2020
# These are my basic imports, I will probably need more later.
from PIL import Image   # I will use this to modify the images.
import openpyxl, requests         # I will use this to make the spread sheet.

# Setting up the api
department_url = 'https://collectionapi.metmuseum.org/public/collection/v1/departments'
departments_data = requests.get(department_url).json()


departments = []
for dic in departments_data['departments']:
    departments.append(dic['displayName'])

