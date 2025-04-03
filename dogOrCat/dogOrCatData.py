#   dog vs cat dataset to do another practice

#   demensions that the resized images should be
RESIZED_DIMENSIONS = (32,32)


#   image processing library
from PIL import Image
import os

#   directory with original cat images
directoryCat = 'dogOrCat/cats'

#   directory with original dog images
directoryDog = 'dogOrCat/dogs'

# If you want only files (not directories), use:
filenamesCat = [f for f in os.listdir(directoryCat) if os.path.isfile(os.path.join(directoryCat, f))]
filenamesDog = [f for f in os.listdir(directoryDog) if os.path.isfile(os.path.join(directoryDog, f))]

# Create directories if they don't exist
os.makedirs("dogOrCat/catsResized", exist_ok=True)
os.makedirs("dogOrCat/dogsResized", exist_ok=True)

# Resize all images into 32x32 and output to another folder
# Not necessary but nice to see the images
for cat in range(len(filenamesCat)):
    img = Image.open("dogOrCat/cats/" + filenamesCat[cat])
    resized = img.resize(RESIZED_DIMENSIONS)
    resized.save("dogOrCat/catsResized/resizedCat" + str(cat) + ".png")

for dog in range(len(filenamesDog)):
    img = Image.open("dogOrCat/dogs/" + filenamesDog[dog])
    resized = img.resize(RESIZED_DIMENSIONS)
    resized.save("dogOrCat/dogsResized/resizedDog" + str(dog) + ".png")

# Convert resized images to linearized RGB arrays (primitive Python lists)
cat_dir = "dogOrCat/catsResized"
dog_dir = "dogOrCat/dogsResized"

data = []  # Each element is (flattened_image_array, one_hot_label)

# Helper function to load and flatten image using primitive lists
def load_and_flatten(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = list(img.getdata())  # list of (R, G, B)
    flat_list = []
    for pixel in pixels:
        flat_list.extend(pixel)  # Add R, G, B individually
    return flat_list  # length = 32*32*3 = 3072

# Process cat images
for filename in sorted(os.listdir(cat_dir)):
    if filename.endswith(".png"):
        path = os.path.join(cat_dir, filename)
        data.append((load_and_flatten(path), [1, 0]))  # One-hot: cat = [1, 0]

# Process dog images
for filename in sorted(os.listdir(dog_dir)):
    if filename.endswith(".png"):
        path = os.path.join(dog_dir, filename)
        data.append((load_and_flatten(path), [0, 1]))  # One-hot: dog = [0, 1]

# Copy inputs and outputs into respective arrays
sampleIns = []
sampleOuts = []
for tup in data:
    sampleIns.append(tup[0])
    sampleOuts.append(tup[1])
