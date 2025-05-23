import os
from PIL import Image
import cupy as cp
from networkGen import NeuralNetwork

from dogOrCatData import RESIZED_DIMENSIONS

# === Load trained model ===
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'catOrDogCUPY1-test.txt')

with open(file_path, "r") as f:
    lines = f.readlines()

structure = list(map(int, lines[0].strip().split()))
network = NeuralNetwork(structure)

lineIdx = 1
for layerInd in range(1, len(structure)):
    for nodeInd in range(structure[layerInd]):
        values = list(map(float, lines[lineIdx].strip().split()))
        lineIdx += 1
        weights = values[:-1]
        bias = values[-1]
        for i, w in enumerate(weights):
            network.setWeight(layerInd - 1, nodeInd, i, w)
        network.setBias(layerInd - 1, nodeInd, bias)

# === Image loader: EXACTLY like training
def load_and_flatten_normalized(image_path):
    img = Image.open(image_path).convert('RGB').resize(RESIZED_DIMENSIONS)
    pixels = list(img.getdata())  # list of (R, G, B)
    flat = [channel / 255.0 for pixel in pixels for channel in pixel]
    return flat

# === Inference loop
print("🐶🐱 Cat or Dog Neural Network Inference")
while True:
    a = input("Path to 32x32 image (.png) or 'q': ")
    if a.lower() == 'q':
        print("Goodbye!")
        break
    try:
        path = os.path.join(script_dir, "testInputPics", a)
        output = network.fullForwardPass(load_and_flatten_normalized(path))
        label = ""
        if output[1] > output[0]:
            if output[1] > .6:
                label = "Dog 🐶 " + str(min(output[1]*100, 100)) + "%"
            else:
                label = "think its a dog but not sure"
        else:
            if output[0] > .6:
                label = "Cat 🐱 " + str(min(output[0]*100, 100)) + "%"
            else:
                label = "thinks its a cat but not sure"
        #print(f"✅ Model output: {output} → Predicted: {label}")
        print()
        print(label)
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
