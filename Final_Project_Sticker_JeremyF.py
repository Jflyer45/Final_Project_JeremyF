# Jeremy Fisher 4/15/2020
# These are my basic imports, I will probably need more later.
from PIL import Image   # I will use this to modify the images.
import openpyxl, requests, random, webbrowser, urllib.request         # I will use this to make the spread sheet.


def ispublicdomain(id):
    collection_url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(id)
    artwork_data = requests.get(collection_url).json()
    if artwork_data['isPublicDomain'] is False:
        return False
    if artwork_data['isPublicDomain'] is True:
        return True


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
object_data = requests.get(objectsurl).json()
total_objects = object_data['total']
objectid_list = object_data['objectIDs']

while True:
    random_number = random.randint(1, total_objects)  # I use this varaible to select a random value from the objectid list!!!
    random_id = objectid_list[random_number]
    if ispublicdomain(random_id) is False:
        continue
    else:
        # Under this I will show the image and see if the user wants it.
        # I NEED TO FIND OUT HOW HE WANTS TO SHOW
        potentartwork_url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(random_id)
        potentartwork_data = requests.get(potentartwork_url).json()
        primaryImageSmall_url = potentartwork_data['primaryImageSmall']
        webbrowser.open(primaryImageSmall_url)
        userinput = input('Do you want this image? (y/n): ').lower()
        if userinput in ['y', 'yes']:
            break
        else:
            continue

primaryImage_url = potentartwork_data['primaryImage']
urllib.request.urlretrieve(primaryImage_url, "chosen_artwork_image.jpg")
image = Image.open('chosen_artwork_image.jpg')
