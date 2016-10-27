import os
import argparse
import pickle
import re
import random
import time

def changeDir(path):
    '''This function changes the directory'''
    os.chdir(path)


def findAllSpamFiles(path):
    #listDir = []
    for dirNamePath, dtory, fileNames in os.walk(path):
        for name in dtory:
            if name == 'spam':
                os.chdir(os.path.join(dirNamePath, name))

                #listDir.extend(pathJoin(os.path.join(dirNamePath, name), os.listdir(os.getcwd())))
                for item in os.listdir(os.getcwd()):
                    yield os.path.join(os.path.join(dirNamePath, name), item)


    #((os.path.join(os.path.join(dirNamePath, name), item))for dirNamePath, dtory, fileNames in os.walk(path) for name in dtory if name == 'spam' for item in os.listdir(os.path.join(dirNamePath, name)))


def findAllHamFiles(path):
    #listDir = []
    for dirNamePath, dtory, fileNames in os.walk(path):
        for name in dtory:
            if name == 'ham':
                os.chdir(os.path.join(dirNamePath, name))
                #listDir.extend(pathJoin(os.path.join(dirNamePath, name), os.listdir(os.getcwd())))
                for item in os.listdir(os.getcwd()):
                    yield os.path.join(os.path.join(dirNamePath, name), item)

    #return listDir





def extractWordsFromSpam(spam, spamIndex):
    weightdictContainer = {}
    wordsForAFileName = {}
    weightWordsList = []
    spamNumber = 0
    #hamNumber = 0

    with open(spam, 'r', encoding="latin1") as fileHandle:
        wordString = fileHandle.read()
        wordList = wordString.split()
        wordListDict = {}
        #weightdictContainer = {word: 0 for word in wordList if word not in weightdictContainer.keys()}
        for word in wordList:
            if word not in weightdictContainer.keys():
                weightdictContainer[word] = 0
            try:
                wordListDict[word] += 1
            except KeyError:
                wordListDict[word] = 1
        spamString = 'spam'+spamIndex.__str__()
        wordsForAFileName[spamString] = wordListDict



    weightWordsList.append(weightdictContainer)
    weightWordsList.append(wordsForAFileName)
    return weightWordsList


def extractWordsFromHam(ham, hamIndex):
    weightdictContainer = {}
    wordsForAFileName = {}
    weightWordsList = []

    #hamNumber = 0

    with open(ham, 'r', encoding="latin1") as fileHandle:
        wordString = fileHandle.read()
        wordList = wordString.split()
        wordListDict = {}
        #weightdictContainer = {word: 0 for word in wordList if word not in weightdictContainer.keys()}
        for word in wordList:
            if word not in weightdictContainer.keys():
                weightdictContainer[word] = 0
            try:
                wordListDict[word] += 1
            except KeyError:
                wordListDict[word] = 1
        hamString = 'ham'+hamIndex.__str__()
        wordsForAFileName[hamString] = wordListDict

    weightWordsList.append(weightdictContainer)
    weightWordsList.append(wordsForAFileName)
    return weightWordsList





def writeModelToFile(bias, weightDict, storePath):
    os.chdir(storePath)
    listPass = [bias, weightDict]
    with open('per_model.txt', mode='wb') as fileHandle:

        pickle.dump(listPass, fileHandle)
    return True


def shuffleContents(weightDict):
    retweightDict = {}
    listOfKeys = list(weightDict.keys())
    random.shuffle(listOfKeys)
    retweightDict = {keyItem : weightDict[keyItem] for keyItem in listOfKeys}

    return retweightDict


if __name__ == '__main__':
    startTime = time.time()
    maxIter = 20
    storePath = os.getcwd()
    parserObj = argparse.ArgumentParser()
    parserObj.add_argument("path_to_folders", help="Specify the path")
    firstArg = parserObj.parse_args()
    direcPath = firstArg.path_to_folders
    #weightDict = {}
    wordsForAFileName = {}
    changeDir(direcPath)

    spamIndex, hamIndex = 0, 0
    weightDict = {}
    #avgWeightDict = {}
    spamFileParsingTime = time.time()
    for file in findAllSpamFiles(direcPath):
        weightWordsList = extractWordsFromSpam(file, spamIndex)
        wordsForAFileName.update(weightWordsList[1])
        weightDict.update(weightWordsList[0])
        spamIndex += 1
    print('spamFileParsingTime: '+(time.time() - spamFileParsingTime).__str__())
    hamFileParsingTime = time.time()
    for file in findAllHamFiles(direcPath):
        weightWordsList = extractWordsFromHam(file, hamIndex)
        wordsForAFileName.update(weightWordsList[1])
        weightDict.update(weightWordsList[0])
        hamIndex += 1
    print('hamFileParsingTime: '+ (time.time() - hamFileParsingTime).__str__())
    #avgWeightDict = dict(weightDict)

    #weightWordsList = extractWordsFromSpamHam(spamFiles, hamFiles)
    #weightDict = weightWordsList[0]
    #wordsForAFileName = weightWordsList[1]
    bias = 0
    i = 0
    #listOfKeys = list(wordsForAFileName.keys())
    while i<maxIter:
        wordsForAFileName = shuffleContents(wordsForAFileName)
        for key, val in wordsForAFileName.items():
            y = 1
            alpha = 0
            for word, x in val.items():
                alpha += (x * weightDict[word])


            alpha += bias

            pattern = re.compile("spam*")
            if pattern.match(key):
                y = 1
            else:
                y = -1


            if alpha*y <= 0:
                bias += y
                for word,x in val.items():

                    weightDict[word] += (y * x)

        i+=1

    if (not writeModelToFile(bias, weightDict ,storePath)):
        print('Model was not exported to per_model.txt')
    print('per_learn file exec time: '+(time.time() - startTime).__str__())


