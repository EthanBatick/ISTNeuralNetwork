# dogOrCatData.py — loads real images into sampleIns and sampleOuts, and saves resized versions

from PIL import Image
import os
import cupy as cp

# Parameters
RESIZED_DIMENSIONS = (32, 32)
base_path = "dogOrCatWithCuPy"
cat_dir = os.path.join(base_path, "cats")
dog_dir = os.path.join(base_path, "dogs")
cat_resized_dir = os.path.join(base_path, "catsResized")
dog_resized_dir = os.path.join(base_path, "dogsResized")

# Ensure resized directories exist
os.makedirs(cat_resized_dir, exist_ok=True)
os.makedirs(dog_resized_dir, exist_ok=True)

data = []

def load_and_flatten_normalized(image_path):
    img = Image.open(image_path).convert('RGB').resize(RESIZED_DIMENSIONS)
    pixels = list(img.getdata())  # list of (R, G, B)
    flat = [channel / 255.0 for pixel in pixels for channel in pixel]
    return flat

# Load and process cat images
for idx, filename in enumerate(sorted(os.listdir(cat_dir))):
    if filename.lower().endswith(".png"):
        path = os.path.join(cat_dir, filename)
        resized = Image.open(path).convert('RGB').resize(RESIZED_DIMENSIONS)
        resized.save(os.path.join(cat_resized_dir, f"resizedCat{idx}.png"))
        data.append((load_and_flatten_normalized(path), [1, 0]))

# Load and process dog images
for idx, filename in enumerate(sorted(os.listdir(dog_dir))):
    if filename.lower().endswith(".png"):
        path = os.path.join(dog_dir, filename)
        resized = Image.open(path).convert('RGB').resize(RESIZED_DIMENSIONS)
        resized.save(os.path.join(dog_resized_dir, f"resizedDog{idx}.png"))
        data.append((load_and_flatten_normalized(path), [0, 1]))

# Split into separate arrays
sampleIns = [cp.array(inp, dtype=cp.float32) for inp, _ in data]
sampleOuts = [cp.array(out, dtype=cp.float32) for _, out in data]
