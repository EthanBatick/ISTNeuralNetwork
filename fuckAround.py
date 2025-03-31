import networkGen

network1 = networkGen.NeuralNetwork([2,4,7])

network1.printNetwork()

print()

network1.setBias(1, 3, 3)

network1.printNetwork()

print(network1.getBias(1,3))