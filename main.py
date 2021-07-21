print("WARNING! IF UR FOLDER NAMES HAVE BRACKETS OR WEIRD CHARACTERS IN THEN THIS MIGHT FUCK UR COMPUTER")

# used for dealing with files/filepaths
import glob, os, shutil

# used for getting file (meta)data
from PIL import Image
# from PIL.ExifTags import TAGS


FILEPATH_DELIMITER="/"

image_formats=["PNG", "JPG"]


from_folder = "/media/bruno/Blade 15/Users/bruno/Documents/GitHub/pic-chooser/images_2"
to_folder = "/media/bruno/Blade 15/Users/bruno/Documents/GitHub/pic-chooser/images"

def get_image_data(img):

    image = Image.open(img)

    return list(image.getdata())

def get_file_extension(filepath):
    assert "." in filepath
    return filepath[filepath.find(".")+1:]



# given 2 image filepaths, determine if they are identical
def images_are_identical(img_1, img_2):

    data_1=get_image_data(img_1)
    data_2=get_image_data(img_2)
    
    # if there is a difference, this will quickly become apparent
    return data_1==data_2

def files_are_identical(file_1, file_2):
    if get_file_extension(file_1) in image_formats and get_file_extension(file_2) in image_formats:
        return images_are_identical(file_1, file_2)
    else:
        return nonimage_files_are_identical(file_1, file_2)

def nonimage_files_are_identical(file_1, file_2):
    return os.path.getsize(file_1)==os.path.getsize(file_2)


# turns /dev/dev/dev/img_12.png into ("/dev/dev/dev", "img_12.png")
def filepath_to_folder_and_file(filepath):

    assert FILEPATH_DELIMITER in filepath and "." in filepath
    components = filepath.split(FILEPATH_DELIMITER)
    return FILEPATH_DELIMITER.join(components[:-1]), components[-1]



def string_between(start, end, s):

    return s[:s.index(start)+len(start):], s[s.index(start)+len(start):s.index(end)], s[s.index(end):]


# give a (not necessarily safe) filepath we can use
# e.g. f("IMG_21.PNG") should return "IMG_21 (1).PNG"
# e.g. f("IMG_21 (5).PNG") should return "IMG_21 (6).PNG"
def duplicate_file_name(path):


    assert "." in path

    folder, filename = filepath_to_folder_and_file(path)

    try:

        # if there is already a set of brackets [ () not )( obviously) ]
        # will throw a ValueError if the
        before, during, after = string_between(" (", ").", filename)

        # and the contents of the brackets are an integer
        n = int(during)

        # reconstruct the filepath, with the integer increased by 1
        return folder+FILEPATH_DELIMITER+before+str(n+1)+after
    
    # if there aren't brackets in the original filename
    except ValueError:

        # put a " (1)" before the "."
        return path[:path.index('.')]+" (1)"+path[path.index('.'):]



# there's probably a better implementation of this for image.getdata() objects
# my_hash=hash


# given an image and a folder, find if the image is already in the folder
# if we find an exact (or very close) duplicate, then return "'DUPLICATE_FOUND', the_filepath_of_the_duplicate, None"
# if we do not find a duplicate, but there is already a file in that folder with that name, then return "NOT_FOUND, None, a_ safe_new_filename"
def find_image_in_folder(image_path, folder):

    # print(f"{image_path=}") # debugging

    # only keep the bit after the final slash
    image_filename = filepath_to_folder_and_file(image_path)[1]

    # print(f"{image_filename=}") # debugging

    potential_new_path=f"{to_folder}{FILEPATH_DELIMITER}{image_filename}" # e.g. (/bruno)(/)(IMG_12.jpg)

    # n=0 # we will rename files with a img_12 (1).png -> img_12 (2).png -> img_12 (3).png -> ... scheme

    # as long as there is a file at the destination we want to copy the image to
    while os.path.exists(potential_new_path):

        print(f"file exists at {potential_new_path}!") # debugging

        # determine if the images are identical
        if files_are_identical(image_path, potential_new_path):

            print("files are identical!")

            return "DUPLICATE_FOUND", potential_new_path, None
        
        else:

            print("files are not identical!")

            potential_new_path=duplicate_file_name(potential_new_path)

    assert not os.path.exists(potential_new_path)

    return "NOT_FOUND", None, potential_new_path

assert images_are_identical("/media/bruno/Elements/PERSONAL_DATA_STORE/PHOTOS_LIKED_FINAL/IMG_E1026 (copy).JPG", "/media/bruno/Elements/PERSONAL_DATA_STORE/PHOTOS_LIKED_FINAL/IMG_E1026 (1).JPG")
assert not images_are_identical("/media/bruno/Elements/PERSONAL_DATA_STORE/PHOTOS_LIKED_FINAL/IMG_E1026 (copy).JPG", "/media/bruno/Elements/PERSONAL_DATA_STORE/PHOTOS_LIKED_FINAL/IMG_E0024 (2).JPG")
assert filepath_to_folder_and_file("/media/bruno/Elements/PERSONAL_DATA_STORE/PHOTOS_LIKED_FINAL/10428594_422651061231059_6026077142475556131_n.jpg") == ("/media/bruno/Elements/PERSONAL_DATA_STORE/PHOTOS_LIKED_FINAL","10428594_422651061231059_6026077142475556131_n.jpg")
assert duplicate_file_name("/dev/dev/IMG_21.PNG") == "/dev/dev/IMG_21 (1).PNG"
assert duplicate_file_name("/dev/dev/IMG_21 (5).PNG") == "/dev/dev/IMG_21 (6).PNG"
assert get_file_extension("/dev/dev/nae.png")=="png"
assert files_are_identical("/media/bruno/Blade 15/Users/bruno/Documents/GitHub/pic-chooser/images_2/ACZX7126.MOV", "/media/bruno/Blade 15/Users/bruno/Documents/GitHub/pic-chooser/images_2/ACZX7126.MOV")
assert files_are_identical("/media/bruno/Blade 15/Users/bruno/Documents/GitHub/pic-chooser/images_2/ACZX7126.MOV","/media/bruno/Blade 15/Users/bruno/Documents/GitHub/pic-chooser/images_2/ACZX7126 (copy).MOV")
assert not files_are_identical("/media/bruno/Blade 15/Users/bruno/Documents/GitHub/pic-chooser/images_2/ACZX7126.MOV", "/media/bruno/Blade 15/Users/bruno/Documents/GitHub/pic-chooser/images_2/ARWH3412.MP4")


from_images=glob.glob(from_folder+f"{FILEPATH_DELIMITER}**")

for image_path in from_images:

    result, duplicate_path, new_path = find_image_in_folder(image_path, to_folder)

    if result=="NOT_FOUND":
        shutil.move(image_path, new_path)
        print(f"moved {image_path} to {new_path}")
    else:
        print(f"not moving {image_path}, as it's identical to {duplicate_path}")
    