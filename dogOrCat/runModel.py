import os
from networkGen import NeuralNetwork
from PIL import Image
from dogOrCatData import RESIZED_DIMENSIONS


#   provide txt file of network model on this line MAKE SURE to add .txt or whatever extension
filename = "catOrDog-16Res-20samples-10Loss.txt"
    

#find model
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, filename)

#open that bitch
with open(file_path, "r") as f:
    lines = f.readlines()

# Read structure into network
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


#   function to compile user provided image to input layer
def load_and_flatten_with_resize(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize(RESIZED_DIMENSIONS)
    pixels = list(img.getdata())  # list of (R, G, B)
    flat_list = []
    for pixel in pixels:
        flat_list.extend(pixel)  # Add R, G, B individually
    return flat_list  # length = 32*32*3 = 3072



#   run user interactive with given model

#   take user input
#   path = str(input("give exact path to image: "))

path = "dogOrCat/testInputPics/testDog0.png"

im1 = load_and_flatten_with_resize(path)

output = network.fullForwardPass(im1)
print(output)
'''
if output[0] > output[1]:
    print("cat")
else:
    print("dog")'''