from variousUtil import dot, activationFunction, outputActivationFunction
import copy
import random

#   object that represents a complete neural network
class NeuralNetwork:
    
    #   'layerStructure' is an array where each element is a 'Layer' objects and 
    #   represents its corresponding layer's number of nodes (DOES include
    #   the input layer so the index 0 refers to the number of params in input layer)
    def __init__(self, networkStructure):
        
        #hold this data to be able to correctly compute dot products
        self.networkStructure = networkStructure
        
        #   'network is an instance variable that holds the
        #   full network where each element is a layer object
        #   IMPORTANT, while 'networkStructure' holds sizes for all
        #   layers including input, 'network' only holds the actual layers
        #   for hidden and output layers because individual input will be
        #   fed in the training algorithm
        self.network = []
        for i in range(1, len(networkStructure)):
            self.network.append(Layer(networkStructure[i], networkStructure[i - 1]))
    
#   getter and setter methods ---------------------------------------
    
    #   zero indexed
    def getWeight(self, layer, node, weight):
        return self.network[layer].layer[node].weights[weight]

    #   zero indexed
    def setWeight(self, layer, node, weight, newWeight):
        self.network[layer].layer[node].weights[weight] = newWeight
        
    #   zero indexed
    def getBias(self, layer, node):
        return self.network[layer].layer[node].bias

    #   zero indexed
    def setBias(self, layer, node, newBias):
        self.network[layer].layer[node].bias = newBias
            
#   -----------------------------------------------------------------
    
    #   returns ouput array of full forward computation of network
    def fullForwardPass(self, input1):
        outputFromLast = copy.deepcopy(input1)
        for i, layer in enumerate(self.network):
            output = []
            for node in layer.layer:
                val = dot(outputFromLast, node.weights) + node.bias
                if i == len(self.network) - 1:
                    output.append(outputActivationFunction(val))  # output layer
                else:
                    output.append(activationFunction(val))         # hidden layers
            outputFromLast = output
        return outputFromLast

        
    
    #   dev function to print the whole network
    def printNetwork(self):
        for layerObj in self.network:
            tempArr = []
            for node in layerObj.layer:
                tempArr.append((node.weights, node.bias))
            print(tempArr)
        
        
        
            
#   layer object that store exactly
#   one layer of 'nodeCount number of 'Node' objects
class Layer:
    
    #   'nodeCount' is integer indicating the number
    #   of nodes in this layer
    def __init__(self, nodeCount, prevNodeCount):
        
        self.layer = []
        for i in range(0, nodeCount):
            self.layer.append(Node(prevNodeCount))
    
    
    
    
#   node object that simply holds
#   a weight and a bias

class Node:
    def __init__(self, prevLayerSize):
        self.bias = random.uniform(-0.1, 0.1)
        self.weights = [random.uniform(-0.1, 0.1) for _ in range(prevLayerSize)]
