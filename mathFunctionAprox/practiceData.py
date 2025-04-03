#   practice data to test the network
#   here we are trying to approximate
#   the functon x^2

data = [([x], [x**2]) for x in range(-20, 21)]


#   copy inputs and outputs into index
#   respective arrays
sampleIns = []
sampleOuts = []
for tup in data:
    sampleIns.append(tup[0])
    sampleOuts.append(tup[1])