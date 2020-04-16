# Jeremy Fisher 4/15/2020
# These are my basic imports, I will probably need more later.
from PIL import Image   # I will use this to modify the images.
import openpyxl, requests, random         # I will use this to make the spread sheet.

# Setting up the api
department_url = 'https://collectionapi.metmuseum.org/public/collection/v1/departments'  # This is the api url
departments_data = requests.get(department_url).json()      # I store the data in a variable, using requests

departments = []                                            # I create an empty string to append to
# The loop below will get every department
for entry in departments_data['departments']:               # For every entry (department) in the department data
    departments.append(entry['displayName'])                # Append the value (department name)

print("Hello! Welcome to Jeremy's Art Sticker Project")     # Welcome text for user
print("Select from one of the following departments, enter a number.")       # Instructs users
print()                                         # Blank space
for x, department in enumerate(departments):    # I create a for loop to display all departments using enumerate
    print(str(x + 1) + ".", department)         # I add 1 to x becuase it starts at 0, and I concatenate it with department.


# Below is users input validation. This makes sure it's a number and a "real" number
while True:
    userinput = input("Enter department number: ")
    try:
        userinput = int(userinput)
    except:
        print("Please use digits and whole numbers!")
        continue
    if userinput > len(departments):
        continue
    if userinput < 1:
        continue
    break

chosen_department = departments[(userinput - 1)]

objectsurl = 'https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=' + str(userinput)
oject_data = requests.get(objectsurl).json()
total_objects = oject_data['total']
random_number = random.randint(0, total_objects)

### I NEED TO MAKE A FUNCTION THAT CHECKS IF THERE IS A PUBLIC IMAGE AVAIBLE!!!


