import os
import argparse
import pickle
import re
import random

def changeDir(path):
    '''This function changes the directory'''
    os.chdir(path)


def pathJoin(dirNamePath, listCon):
    returnList = []
    for item in listCon:
        returnList.append(os.path.join(dirNamePath, item))
    return returnList

def findAllSpamFiles(path):
    listDir = []
    for dirNamePath, dtory, fileNames in os.walk(path):
        for name in dtory:
            if name == 'spam':
                os.chdir(os.path.join(dirNamePath, name))

                listDir.extend(pathJoin(os.path.join(dirNamePath, name), os.listdir(os.getcwd())))

    return listDir




def findAllHamFiles(path):
    listDir = []
    for dirNamePath, dtory, fileNames in os.walk(path):
        for name in dtory:
            if name == 'ham':
                os.chdir(os.path.join(dirNamePath, name))
                listDir.extend(pathJoin(os.path.join(dirNamePath, name), os.listdir(os.getcwd())))

    return listDir





def extractWordsFromSpamHam(spampath, hampath):
    weightdictContainer = {}
    wordsForAFileName = {}
    weightWordsList = []
    spamNumber = 0
    hamNumber = 0
    for item in spampath:
        with open(item, 'r', encoding="latin1") as fileHandle:
            wordString = fileHandle.read()
            wordList = wordString.split()
            wordListDict = {}
            weightdictContainer = {word:0 for word in wordList if word not in weightdictContainer.keys()}
            #wordListDict = {word:}
            for word in wordList:
                #if word not in weightdictContainer.keys():
                    #weightdictContainer[word] = 0
                if word not in wordListDict.keys():
                    wordListDict[word] = 1
                else:
                    wordListDict[word] += 1
            spamString = 'spam'+spamNumber.__str__()
            wordsForAFileName[spamString] = wordListDict

            spamNumber += 1
    #print(len(wordsForAFileName))


    for item in hampath:
        with open(item, 'r', encoding="latin1") as fileHandle:
            wordString = fileHandle.read()
            wordList = wordString.split()
            wordListDict = {}
            #weightdictContainer = {word: 0 for word in wordList if word not in weightdictContainer.keys()}
            for word in wordList:
                if word not in weightdictContainer.keys():
                    weightdictContainer[word] = 0
                if word not in wordListDict.keys():
                    wordListDict[word] = 1
                else:
                    wordListDict[word] += 1
            hamString = 'ham'+ hamNumber.__str__()
            wordsForAFileName[hamString] = wordListDict
            hamNumber += 1
    #print(len(wordsForAFileName))
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

    for keyItem in listOfKeys:
        retweightDict[keyItem] = weightDict[keyItem]
    return retweightDict


if __name__ == '__main__':
    maxIter = 20
    storePath = os.getcwd()
    parserObj = argparse.ArgumentParser()
    parserObj.add_argument("path_to_folders", help="Specify the path")
    firstArg = parserObj.parse_args()
    direcPath = firstArg.path_to_folders
    weightDict = {}
    wordsForAFileName = {}
    changeDir(direcPath)

    spamFiles = findAllSpamFiles(direcPath)


    hamFiles = findAllHamFiles(direcPath)

    weightWordsList = extractWordsFromSpamHam(spamFiles, hamFiles)
    weightDict = weightWordsList[0]
    wordsForAFileName = weightWordsList[1]
    bias = 0
    i = 0

    while i<maxIter:
        wordsForAFileName = shuffleContents(wordsForAFileName)
        for key, val in wordsForAFileName.items():
            y = 1
            alpha = 0
            for word, x in val.items():
                if word in weightDict.keys():
                    alpha += x * weightDict[word]


            alpha += bias

            pattern = re.compile("spam*")
            if pattern.match(key):
                y = 1
            else:
                y = -1


            if alpha*y <= 0:
                bias += y
                for word,x in val.items():
                    if word in weightDict.keys():
                        weightDict[word] += (y * x)

        i+=1

    if (not writeModelToFile(bias, weightDict ,storePath)):
        print('Model was not exported to per_model.txt')


