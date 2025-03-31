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
    #   define activation function for the network here
    return x