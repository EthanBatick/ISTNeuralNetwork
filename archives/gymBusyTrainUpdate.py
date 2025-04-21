import copy
import random
from gymBusyData import sampleIns, sampleOuts
import networkGen
from variousUtil import lossDiffSquared
import os


#   changeWeights and changeBiases will half after this many passes of the entire network
DIVIDE_AFTER_PASSES = 8


#   make TARGET_LOSS = PERSERVERANCE_LOSS to prevent stagnation
TARGET_LOSS = 6
PERSERVERE_LOSS = 6
MAX_ATTEMPTS = 10
structure = [3,20,10,1]
mainNetwork = networkGen.NeuralNetwork(structure)

#   file that trained network data will save to
weightsSaveFile = 'gymBusy-300SamplesWithAM-6Loss.txt'

def trainModel(mainNetwork, structure):
    

    sampleInputs = copy.deepcopy(sampleIns)
    sampleOutputs = copy.deepcopy(sampleOuts)

    changeBias = .5
    changeWeight = .1
    cleanExit = False
    bestLoss = float('inf')

    # Stagnation detection
    previousLoss = None
    stagnationCounter = 0
    stagnationThreshold = 0.000  # 0.0% relative change aka it goes forever
    stagnationLimit = 3
    hardBreak = False
    count = 0
    while True:
        if hardBreak:
            break
        count += 1
        if count % DIVIDE_AFTER_PASSES == 0:
            changeBias/=2
            changeWeight/=2

        for layerInd in range(1, len(structure)):

            for nodeInd in range(structure[layerInd]):
                changeBiasImproved = False
                changeWeightImproved = False


                #   TODO
                '''
                # Bias tweak
                networkUpB = copy.deepcopy(mainNetwork)
                networkUpB.setBias(layerInd - 1, nodeInd,
                    mainNetwork.getBias(layerInd - 1, nodeInd) + changeBias)
                networkDownB = copy.deepcopy(mainNetwork)
                networkDownB.setBias(layerInd - 1, nodeInd,
                    mainNetwork.getBias(layerInd - 1, nodeInd) - changeBias)
                #   TODO end
                '''

                #   set the up and down biases
                stayB = mainNetwork.getBias(layerInd - 1, nodeInd)
                upB = mainNetwork.getBias(layerInd - 1, nodeInd) + changeBias
                downB = mainNetwork.getBias(layerInd - 1, nodeInd) - changeBias

                lossMain = lossUp = lossDown = 0

                #   calc loss without changes
                for i in range(len(sampleInputs)):
                    lossMain += lossDiffSquared(mainNetwork.fullForwardPass(sampleInputs[i]), sampleOutputs[i])

                #   calc loss with up tweak
                for i in range(len(sampleInputs)):
                    mainNetwork.setBias(layerInd - 1, nodeInd, upB)
                    lossUp += lossDiffSquared(mainNetwork.fullForwardPass(sampleInputs[i]), sampleOutputs[i])

                #   calc loss with down tweak
                for i in range(len(sampleInputs)):
                    mainNetwork.setBias(layerInd - 1, nodeInd, downB)
                    lossDown += lossDiffSquared(mainNetwork.fullForwardPass(sampleInputs[i]), sampleOutputs[i])


                if lossMain < bestLoss:
                    bestLoss = lossMain

                if lossMain < lossUp and lossMain < lossDown:
                    #   set network back to original
                    mainNetwork.setBias(layerInd - 1, nodeInd, stayB)

                elif lossUp < lossDown:
                    #   TODO
                    mainNetwork.setBias(layerInd - 1, nodeInd, upB)
                    changeBiasImproved = True
                else:
                    #   TODO
                    mainNetwork.setBias(layerInd - 1, nodeInd, downB)
                    changeBiasImproved = True

                for weightInd in range(structure[layerInd - 1]):

                    #   TODO 

                    lossMain = lossUp = lossDown = 0

                    #   set the up and down biases
                    stayW = mainNetwork.getWeight(layerInd - 1, nodeInd, weightInd)
                    upW = mainNetwork.getWeight(layerInd - 1, nodeInd, weightInd) + changeWeight
                    downW = mainNetwork.getWeight(layerInd - 1, nodeInd, weightInd) - changeWeight

                    #   TODO

                    #   calc loss without changes
                    for i in range(len(sampleInputs)):
                        lossMain += lossDiffSquared(mainNetwork.fullForwardPass(sampleInputs[i]), sampleOutputs[i])

                    #   calc loss with up tweak
                    for i in range(len(sampleInputs)):
                        mainNetwork.setWeight(layerInd - 1, nodeInd, weightInd, upW)
                        lossUp += lossDiffSquared(mainNetwork.fullForwardPass(sampleInputs[i]), sampleOutputs[i])

                    #   calc loss with down tweak
                    for i in range(len(sampleInputs)):
                        mainNetwork.setWeight(layerInd - 1, nodeInd, weightInd, downW)
                        lossDown += lossDiffSquared(mainNetwork.fullForwardPass(sampleInputs[i]), sampleOutputs[i])


                    if lossMain < bestLoss:
                        bestLoss = lossMain

                    if lossMain < lossUp and lossMain < lossDown:
                        #   set network back to original
                        mainNetwork.setWeight(layerInd - 1, nodeInd, weightInd, stayW)

                    elif lossUp < lossDown:
                        #   TODO
                        mainNetwork.setWeight(layerInd - 1, nodeInd, weightInd, upW)
                        changeWeightImproved = True
                        lossMain = lossUp
                    else:
                        #   TODO
                        mainNetwork.setWeight(layerInd - 1, nodeInd, weightInd, downW)
                        changeWeightImproved = True
                        lossMain = lossDown

                    if weightInd % 1 == 0:
                        print(layerInd,nodeInd, weightInd, lossMain, changeWeight, changeBias, changeWeightImproved, changeBiasImproved)
                        #print(layerInd, bestLoss)

                    if bestLoss < TARGET_LOSS:
                        print("✅ Reached target loss. Done training!")
                        cleanExit = True
                        return mainNetwork, bestLoss
                    
                    




        print(f"Current loss: {lossMain:.2f} | Best: {bestLoss:.2f}")

        # ✅ Stagnation detection (relative)
        if previousLoss is not None:
            delta = abs(lossMain - previousLoss) / (lossMain + 1e-8)
            if delta < stagnationThreshold:
                if lossMain > PERSERVERE_LOSS:
                    stagnationCounter += 1
                    print(f"⚠️  Loss change Δ{delta:.5f} is small — {stagnationCounter}/{stagnationLimit}")
                else:
                    print("stagnation but perserverance hit. Loss: ", lossMain)
            else:
                stagnationCounter = 0
        previousLoss = lossMain

        if stagnationCounter >= stagnationLimit and bestLoss > TARGET_LOSS and bestLoss > PERSERVERE_LOSS:
            print("😴 Training is asymptotic and still above target loss — restarting...")
            return None

        # Jitter if fully stuck
        if changeBias < 1e-6 and changeWeight < 1e-6:
            jitter_scale = 0.01
            print(f"⚡ Injecting jitter (±{jitter_scale:.5f}) to escape local min...")

            for layerInd in range(1, len(structure)):
                for nodeInd in range(structure[layerInd]):
                    for weightInd in range(structure[layerInd - 1]):
                        w = mainNetwork.getWeight(layerInd - 1, nodeInd, weightInd)
                        mainNetwork.setWeight(layerInd - 1, nodeInd, weightInd,
                            w + random.uniform(-jitter_scale, jitter_scale))
                    b = mainNetwork.getBias(layerInd - 1, nodeInd)
                    mainNetwork.setBias(layerInd - 1, nodeInd,
                        b + random.uniform(-jitter_scale, jitter_scale))

            changeBias = 0.1
            changeWeight = 0.1

    return mainNetwork, bestLoss if cleanExit else None


# 🔁 Auto-retry training loop
attempts = 0
model = None

while attempts < MAX_ATTEMPTS:
    print(f"\n🚀 Starting training attempt #{attempts + 1}...")
    result = trainModel(mainNetwork, structure)

    if result is not None:
        model, bestLoss = result
        if bestLoss < TARGET_LOSS:
            print(f"✅ Model converged with loss {bestLoss:.2f} — success!\n")
            break
        else:
            print(f"⚠️ Model got stuck at loss {bestLoss:.2f} — restarting...")
    else:
        print("💥 Training stagnated. Terminating and recording")
        break

    attempts += 1



#   write trained data into a file to store weights and biases

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, weightsSaveFile)
dataFile = open(file_path, 'w')


# Write structure
dataFile.write(" ".join(map(str, structure)) + "\n")
print("recording")

# Write each node's weights + bias in a single line
for layerInd in range(1, len(structure)):
    for nodeInd in range(structure[layerInd]):
        weights = [model.getWeight(layerInd - 1, nodeInd, i) for i in range(structure[layerInd - 1])]
        bias = model.getBias(layerInd - 1, nodeInd)
        nodeData = weights + [bias]
        dataFile.write(" ".join(map(str, nodeData)) + "\n")


dataFile.close()

print("sample count: " + str(len(sampleOuts)))