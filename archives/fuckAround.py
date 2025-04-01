import networkGen

network1 = networkGen.NeuralNetwork([2,3,2])
network1.setWeight(0, 1, 1, 2.5)
network1.setBias(1, 0, 1.0)

network1.printNetwork()
print()
print(network1.fullForwardPass([1.0,2.0]))