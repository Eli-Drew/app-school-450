
def splitDataSet(data, endOfTrainingSet):
    package = []
    trainingSet = data[:endOfTrainingSet]
    testSet = data[endOfTrainingSet:]
    package.append(trainingSet)
    package.append(testSet)
    
    return package

def main():
    pass

if __name__ == "__main__":
    main()