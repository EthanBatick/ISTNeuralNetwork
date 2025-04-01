import os
from networkGen import NeuralNetwork


#   provide txt file of network model on this line MAKE SURE to add .txt or whatever extension

filename = "irisModel1.txt"
    

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
print("X Squared neural network approximater:")
while True:
    
    #   take user input
    sl = input("Input Sepal Length in cm: ")
    sw = input("Input Sepal Width in cm: ")
    pl = input("Input Petal Length in cm: ")
    pw = input("Input Petal Width in cm: ")
    
    output = network.fullForwardPass([float(sl),float(sw),float(pl),float(pw)])
    if output[0] > output[1] and output[0] > output[2]:
        print("setosa")
    elif output[1] > output[0] and output[1] > output[2]:
        print("versicolo")
    else:
        print("virginica")