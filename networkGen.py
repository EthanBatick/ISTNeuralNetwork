from variousUtil import dot

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
        self.bias = 0.0
        self.weights = []
        for i in range(prevLayerSize):
            self.weights.append(1.0)