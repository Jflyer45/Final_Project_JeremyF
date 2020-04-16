# Jeremy Fisher 4/15/2020
# These are my basic imports, I will probably need more later.
from PIL import Image   # I will use this to modify the images.
import openpyxl, requests, random, urllib.request, os, datetime         # I will use this to make the spread sheet.
from openpyxl import Workbook

def ispublicdomain(id):
    collection_url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(id)
    artwork_data = requests.get(collection_url).json()
    if artwork_data['isPublicDomain'] is False:
        return False
    if artwork_data['isPublicDomain'] is True:
        return True

# Below is users input validation. This makes sure it's a number and a "real" number
def makedigitandrange(min, max):
    while True:
        userinput = input("Enter a number: ")
        try:
            userinput = int(userinput)
        except:
            print("Please use digits and whole numbers!")
            continue
        if userinput > max:
            continue
        if userinput < min:
            continue
        return userinput


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

userinput = makedigitandrange(1, len(departments))


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
        urllib.request.urlretrieve(primaryImageSmall_url, "TempImage.jpg")
        thumbnail = Image.open('TempImage.jpg')
        thumbnail.show()
        userinput = input('Do you want this image? (y/n): ').lower()
        if userinput in ['y', 'yes']:
            os.remove('TempImage.jpg')
            break
        else:
            continue

primaryImage_url = potentartwork_data['primaryImage']
urllib.request.urlretrieve(primaryImage_url, "chosen_artwork_image.jpg")
image = Image.open('chosen_artwork_image.jpg')

stickers = os.listdir('Stickers')

print()
print("Chose a meme sticker or select random")

for x, sticker in enumerate(stickers):
    print(str(x + 1) + ".", sticker[:-4])
print("5. Random")

userinput = makedigitandrange(1, (len(stickers) + 1))

if userinput == (len(stickers) + 1):
    userinput = random.randint(1, len(stickers))

selected_sticker = stickers[userinput - 1]

sticker = Image.open('Stickers\\' + selected_sticker)

# I will probaby need to resize the the sticker to thumbnail size
width, height = image.width, image.height
print(height, width)
sticker.resize((round(width * .125), round(height * .125)))


#TO DO--- FIGURE OUT MATH




image.paste(sticker, (0, 100))
image.show()
# I need to figure out pasteing

try:
    workbook = openpyxl.load_workbook('StickerArtSheet.xlsx')
    workbook.close()
except:
    workbook = Workbook()
    sheet = workbook.active  # Make the sheet active
    sheet.cell(1, 1, 'Title')
    sheet.cell(1, 2, "Artist")
    sheet.cell(1, 3, "URL")
    sheet.cell(1, 4, 'Sticker')
    sheet.cell(1, 5, 'Date & Time')
    workbook.save('StickerArtSheet.xlsx')
    workbook.close()

artbook = openpyxl.load_workbook('StickerArtSheet.xlsx')
artsheet = artbook.active

artist = potentartwork_data['artistDisplayName']
if artist == '':
    artist = "Unknown or N/A"

workbook_data = [str(potentartwork_data['title']), artist, str(primaryImage_url),
                 str(selected_sticker), str(datetime.datetime.today())]

columns_list = list(artsheet.columns)
columns1 = columns_list[0]
row = len(columns1) + 1

#for index, data in enumerate(sheet):
    #sheet.cell(row, index + 1, data)

for thing in workbook_data:
    print(thing)

# Until I figure out the loop error, I'm keeping this code
artsheet.cell(row, 1, potentartwork_data['title'])
artsheet.cell(row, 2, artist)
artsheet.cell(row, 3, primaryImage_url)
artsheet.cell(row, 4, selected_sticker)
artsheet.cell(row, 5, datetime.datetime.today())
artbook.save('StickerArtSheet.xlsx')