import os
from networkGen import NeuralNetwork


#   provide txt file of network model on this line MAKE SURE to add .txt or whatever extension
filename = "xSquaredMinus10-20Loss.txt"
    

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


#   run user interactive with given model
print("Math Function neural network approximater:")
while True:
    
    #   take user input
    a = input("Input a number ('q' to exit): ")
    
    
    if a == 'q':
    #   exit condition
        print("goodbye!")
        break
    
    else:
        print("network output: ", network.fullForwardPass([float(a)])[0])