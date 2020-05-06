# Jeremy Fisher 4/15/2020
# These are my basic imports, I will probably need more later.
from PIL import Image   # I will use this to modify the images.
import openpyxl, requests, random, urllib.request, os, datetime
from openpyxl import Workbook

# Validation of the selected object to make sure it's in the public domain.
def ispublicdomain(id):
    collection_url = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(id)
    try:
        artwork_data = requests.get(collection_url).json()
    except:
        print("Couldn't reach the server. Try checking your internet and re-run this program")
        exit()
    if artwork_data['isPublicDomain'] is False:
        return False
    if artwork_data['isPublicDomain'] is True:
        return True


# Below is users input validation. This makes sure it's a number and a "real" number
def digit_and_range_validation(min, max):
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


# Validation to make sure the user doesn't chose an empty department.
def emptydepartmentcheck(url):
    try:
        object_data = requests.get(url).json()
    except:
        print("Couldn't reach the server. Try checking your internet and re-run this program")
        exit()
    if object_data['total'] == 0:
        return True
    else:
        return False

def main():
    # Setting up the api
    department_url = 'https://collectionapi.metmuseum.org/public/collection/v1/departments'  # This is the api url
    try:
        departments_data = requests.get(department_url).json()      # I store the data in a variable, using requests
    except:
        print("Couldn't reach the server. Try checking your internet and re-run this program")
        exit()

    departments = []                                            # I create an empty string to append to
    # The loop below will get every department
    for entry in departments_data['departments']:               # For every entry (department) in the department data
        departments.append(entry['displayName'])                # Append the value (department name)

    print("Hello! Welcome to Jeremy's Art Sticker Project")     # Welcome text for user
    print("Select from one of the following departments, enter a number.")       # Instructs users
    print()                                         # Blank space
    for x, department in enumerate(departments):    # I create a for loop to display all departments using enumerate
        print(str(x + 1) + ".", department)         # I add 1 to x becuase it starts at 0, and I concatenate it with department.

    while True:
        userinput = digit_and_range_validation(1, len(departments))
        collectionurl = 'https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds='
        if emptydepartmentcheck((collectionurl + str(userinput))) is True:
            print("Unfortunally, at this time the department you have selected has no works of art, chose another one.")
            continue
        else:
            break

    objectsurl = collectionurl + str(userinput)
    try:
        object_data = requests.get(objectsurl).json()
    except:
        print("Couldn't reach the server. Try checking your internet and re-run this program")
        exit()
    chosen_department = departments[(userinput - 1)]

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
            try:
                potentartwork_data = requests.get(potentartwork_url).json()
            except:
                print("Couldn't reach the server. Try checking your internet and re-run this program")
                exit()
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
    try:
        urllib.request.urlretrieve(primaryImage_url, "chosen_artwork_image.jpg")
    except:
        print("Couldn't reach the server. Try checking your internet and re-run this program")
        exit()
    image = Image.open('chosen_artwork_image.jpg')

    stickers = os.listdir('Stickers')

    print()
    print("Chose a meme sticker or select random")

    for x, sticker in enumerate(stickers):
        print(str(x + 1) + ".", sticker[:-4])
    print("5. Random")

    userinput = digit_and_range_validation(1, (len(stickers) + 1))

    if userinput == (len(stickers) + 1):
        userinput = random.randint(1, len(stickers))

    selected_sticker = stickers[userinput - 1]

    try:
        sticker = Image.open('Stickers\\' + selected_sticker, )
    except:
        print("Couldn't find the Stickers folder. Make sure to download it, and not change the name. Keep it in the same "
              "folder as the python program.")

    # I will probaby need to resize the the sticker to thumbnail size
    width, height = image.width, image.height
    sticker.resize((round(width * .125), round(height * .125)))
    sticker = sticker.rotate(random.randint(-360, 360))


    #TO DO--- FIGURE OUT MATH

    x_axis = random.randint(0, height - round((height * .125)))
    y_axis = random.randint(0, width - round((width * .125)))

    image.paste(sticker.convert('RGBA'), (x_axis, y_axis), sticker.convert('RGBA'))

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

main()
