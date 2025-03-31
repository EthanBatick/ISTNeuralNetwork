#   object that represents a complete neural network
class NeuralNetwork:
    
    #   'layerStructure' is an array where each element is a 'Layer' objects and 
    #   represents its corresponding layer's number of nodes (DOES NOT include
    #   the input layer so the index 0 refers to the first hidden layer)
    def __init__(self, layerStructure):
        
        #   'network is an instance variable that holds the
        #   full network where each element is a layer object
        self.network = []
        for layerSize in layerStructure:
            self.network.append(Layer(layerSize))
            
    def printNetwork(self):
        for layerObj in self.network:
            tempArr = []
            for node in layerObj.layer:
                tempArr.append((node.weight, node.bias))
            print(tempArr)
        
        
        
            
#   layer object that store exactly
#   one layer of 'nodeCount number of 'Node' objects
class Layer:
    
    #   'nodeCount' is integer indicating the number
    #   of nodes in this layer
    def __init__(self, nodeCount):
        
        self.layer = []
        for i in range(nodeCount):
            self.layer.append(Node())
    
    
    
    
#   node object that simply holds
#   a weight and a bias
class Node:
    def __init__(self):
        self.weight = 1.0
        self.bias = 0.0