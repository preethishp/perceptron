import os
import argparse
import pickle
import re
import random

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




def writeModelToFile(avgBias, avgWeightDict, storePath):
    os.chdir(storePath)
    listPass = [avgBias, avgWeightDict]
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
    maxIter = 30
    storePath = os.getcwd()
    parserObj = argparse.ArgumentParser()
    parserObj.add_argument("path_to_folders", help="Specify the path")
    firstArg = parserObj.parse_args()
    direcPath = firstArg.path_to_folders

    wordsForAFileName = {}
    changeDir(direcPath)

    #spamFiles = findAllSpamFiles(direcPath) #TODO: Generators can be used here. Instead of generating a huge list of spam and ham files. A file can be processed one at a time.


    #hamFiles = findAllHamFiles(direcPath)
    spamIndex, hamIndex = 0, 0
    weightDict = {}
    avgWeightDict = {}

    for file in findAllSpamFiles(direcPath):
        #weightWordsList = extractWordsFromSpam(file, spamIndex)
        wordsForAFileName.update(extractWordsFromSpam(file, spamIndex)[1])
        weightDict.update(extractWordsFromSpam(file, spamIndex)[0])
        spamIndex += 1



    for file in findAllHamFiles(direcPath):

        wordsForAFileName.update(extractWordsFromHam(file, hamIndex)[1])
        weightDict.update(extractWordsFromHam(file, hamIndex)[0])
        hamIndex += 1

    avgWeightDict = dict(weightDict)

    bias = 0
    avgBias = 0
    i = 0
    count = 1


    while i<maxIter:
        wordsForAFileName = shuffleContents(wordsForAFileName)
        for key, val in wordsForAFileName.items():
            y = 1
            alpha = 0
            for word, x in val.items():
                alpha += x * weightDict[word]


            alpha += bias

            pattern = re.compile("spam*")
            if pattern.match(key):
                y = 1
            else:
                y = -1

            if alpha*y <= 0:
                bias += y
                avgBias += (y*count)
                for word,x in val.items():
                    weightDict[word] += (y * x)
                    avgWeightDict[word] += (y * count * x)

            count+=1

        i+=1



    avgBias = bias - ((1/count) * avgBias)
    #for keyValue in avgWeightDict.keys():
        #avgWeightDict[keyValue] = weightDict[keyValue] - ((1/count)*avgWeightDict[keyValue])

    avgWeightDict = {keyValue : (weightDict[keyValue] - ((1/count)*avgWeightDict[keyValue])) for keyValue in avgWeightDict.keys()}


    if (not writeModelToFile(avgBias, avgWeightDict, storePath)):
        print('Model was not exported to per_model.txt')

