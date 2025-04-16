import os
from PIL import Image
import cupy as cp
from networkGen import NeuralNetwork

# === Load trained model ===
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'gymBusy-300Samples-3Loss.txt')

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

# === Inference loop
#turned into method so the UI can easily call
print("Gym business predictor!")
def predict(hour, ampm, day):
    #hour = int(input('hour (0–11) → morning/evening 12-hour format: '))
    #ampm = int(input('(0 = AM, 1 = PM): '))
    #day = int(input('(0 = Monday, ..., 6 = Sunday)'))

    tup = (hour, ampm, day)

    return network.fullForwardPass(tup)[0]*100

    #print(str(round(network.fullForwardPass(tup)[0]*100, 1)) + "% full")