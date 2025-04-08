import cupy as cp

def activationFunction(x):
    return cp.maximum(0, x)  # ReLU

class Node:
    def __init__(self, prevLayerSize):
        self.bias = cp.array(cp.random.normal(loc=0.0, scale=0.05).item(), dtype=cp.float32)
        self.weights = cp.random.normal(loc=0.0, scale=0.05, size=prevLayerSize).astype(cp.float32)


class Layer:
    def __init__(self, nodeCount, prevNodeCount):
        self.layer = [Node(prevNodeCount) for _ in range(nodeCount)]

class NeuralNetwork:
    def __init__(self, networkStructure):
        self.networkStructure = networkStructure
        self.network = [Layer(networkStructure[i], networkStructure[i - 1])
                        for i in range(1, len(networkStructure))]

    def getWeight(self, layer, node, weight):
        return float(self.network[layer].layer[node].weights[weight])

    def setWeight(self, layer, node, weight, newWeight):
        self.network[layer].layer[node].weights[weight] = cp.float32(newWeight)

    def getBias(self, layer, node):
        return float(self.network[layer].layer[node].bias)

    def setBias(self, layer, node, newBias):
        self.network[layer].layer[node].bias = cp.array([newBias], dtype=cp.float32)

    def fullForwardPass(self, input1):
        output = cp.array(input1, dtype=cp.float32).flatten()
        for layer in self.network:
            next_output = []
            for node in layer.layer:
                val = activationFunction(cp.dot(node.weights, output) + node.bias)
                next_output.append(val.reshape(1))  # FIXED: ensure shape is (1,)
            output = cp.concatenate(next_output, axis=0).astype(cp.float32)
        return output.get().tolist()
