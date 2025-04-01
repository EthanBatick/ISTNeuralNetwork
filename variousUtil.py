#   simple dot product helper function between two arrays
def dot(arr1, arr2):
    if len(arr1) != len(arr2):
        raise Exception("array sizes do not match")
    else:
        sum1 = 0.0
        for i in range(len(arr1)):
            sum1 += arr1[i] * arr2[i]
        return sum1
    
def activationFunction(x):
    return max(0, x)

def outputActivationFunction(x):
    return x


#   possible lost function to compare network generation accuracy
def lossDiffSquared(out, target):
    if len(out) != len(target):
        raise Exception("array lengths do not match")
    else:
        sumDiff = 0
        for i in range(len(out)):
            sumDiff += (out[i] - target[i])**2
        return sumDiff
