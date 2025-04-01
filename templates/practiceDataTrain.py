import copy
import random
#i  mport samples as 'sampleIns' and 'sampleOuts' here!
from networkGen import NeuralNetwork
from variousUtil import lossDiffSquared

#   make TARGET_LOSS = PERSERVERANCE_LOSS to prevent stagnation
TARGET_LOSS = 100
PERSERVERE_LOSS = 100

MAX_ATTEMPTS = 100

def trainModel():
    structure = [1, 15, 10, 5, 1]
    mainNetwork = networkGen.NeuralNetwork(structure)

    sampleInputs = copy.deepcopy(sampleIns)
    sampleOutputs = copy.deepcopy(sampleOuts)

    changeBias = 0.1
    changeWeight = 0.1
    cleanExit = False
    bestLoss = float('inf')

    # Stagnation detection
    previousLoss = None
    stagnationCounter = 0
    stagnationThreshold = 0.0005  # 0.05% relative change
    stagnationLimit = 3

    while True:
        changeBiasImproved = False
        changeWeightImproved = False

        for layerInd in range(1, len(structure)):
            for nodeInd in range(structure[layerInd]):
                # Bias tweak
                networkUpB = copy.deepcopy(mainNetwork)
                networkUpB.setBias(layerInd - 1, nodeInd,
                    mainNetwork.getBias(layerInd - 1, nodeInd) + changeBias)
                networkDownB = copy.deepcopy(mainNetwork)
                networkDownB.setBias(layerInd - 1, nodeInd,
                    mainNetwork.getBias(layerInd - 1, nodeInd) - changeBias)

                lossMain = lossUp = lossDown = 0
                for i in range(len(sampleInputs)):
                    lossMain += lossDiffSquared(mainNetwork.fullForwardPass(sampleInputs[i]), sampleOutputs[i])
                    lossUp += lossDiffSquared(networkUpB.fullForwardPass(sampleInputs[i]), sampleOutputs[i])
                    lossDown += lossDiffSquared(networkDownB.fullForwardPass(sampleInputs[i]), sampleOutputs[i])

                if lossMain < bestLoss:
                    bestLoss = lossMain

                if lossMain < lossUp and lossMain < lossDown:
                    pass  # no improvement
                elif lossUp < lossDown:
                    mainNetwork = copy.deepcopy(networkUpB)
                    changeBiasImproved = True
                else:
                    mainNetwork = copy.deepcopy(networkDownB)
                    changeBiasImproved = True

                for weightInd in range(structure[layerInd - 1]):
                    networkUpW = copy.deepcopy(mainNetwork)
                    networkUpW.setWeight(layerInd - 1, nodeInd, weightInd,
                        mainNetwork.getWeight(layerInd - 1, nodeInd, weightInd) + changeWeight)
                    networkDownW = copy.deepcopy(mainNetwork)
                    networkDownW.setWeight(layerInd - 1, nodeInd, weightInd,
                        mainNetwork.getWeight(layerInd - 1, nodeInd, weightInd) - changeWeight)

                    lossMain = lossUp = lossDown = 0
                    for i in range(len(sampleInputs)):
                        lossMain += lossDiffSquared(mainNetwork.fullForwardPass(sampleInputs[i]), sampleOutputs[i])
                        lossUp += lossDiffSquared(networkUpW.fullForwardPass(sampleInputs[i]), sampleOutputs[i])
                        lossDown += lossDiffSquared(networkDownW.fullForwardPass(sampleInputs[i]), sampleOutputs[i])

                    if lossMain < bestLoss:
                        bestLoss = lossMain

                    if lossMain < lossUp and lossMain < lossDown:
                        pass  # no improvement
                    elif lossUp < lossDown:
                        mainNetwork = copy.deepcopy(networkUpW)
                        changeWeightImproved = True
                    else:
                        mainNetwork = copy.deepcopy(networkDownW)
                        changeWeightImproved = True

        # Shrink steps only if no improvement at all
        if not changeBiasImproved:
            changeBias = max(changeBias / 2, 1e-6)
        if not changeWeightImproved:
            changeWeight = max(changeWeight / 2, 1e-6)

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

        if bestLoss < TARGET_LOSS:
            print("✅ Reached target loss. Done training!")
            cleanExit = True
            break

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
    result = trainModel()

    if result is not None:
        model, bestLoss = result
        if bestLoss < TARGET_LOSS:
            print(f"✅ Model converged with loss {bestLoss:.2f} — success!\n")
            break
        else:
            print(f"⚠️ Model got stuck at loss {bestLoss:.2f} — restarting...")
    else:
        print("💥 Training failed. Retrying...")

    attempts += 1

# 🧪 Interactive testing
if model is None or bestLoss >= TARGET_LOSS:
    print("❌ Could not train a good model after several attempts.")
else:
    print("🎉 Training complete! Test your model:")
    while True:
        try:
            user_input = input("Enter a number (or 'q' to quit): ")
            if user_input.lower() == 'q':
                break
            x = float(user_input)
            prediction = model.fullForwardPass([x])[0]
            print(f"Model says: {prediction:.4f}  |  Actual x²: {x**2:.4f}")
        except:
            print("Invalid input.")
