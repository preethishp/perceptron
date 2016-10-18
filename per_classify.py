import os
import argparse
import fnmatch
import pickle


def changeDir(path):
    os.chdir(path)

def findAllFiles(path):
    allFiles = [os.path.join(pathDir, filename)
                 for pathDir, namedir, tfiles in os.walk(path)
                 for filename in fnmatch.filter(tfiles, '*.txt')]
    return allFiles



def openModel(storePath):
    os.chdir(storePath)
    listPass = []
    with open('per_model.txt','rb') as fileHandle:
        listPass = pickle.loads(fileHandle.read(), encoding='latin1')
    return listPass

def extractKeyWords(fileParam):
    wordDict = {}
    with open(fileParam, 'r', encoding='latin1') as fileHandle:
        wordList = fileHandle.read().split()
        for word in wordList:
            if word not in wordDict:
                wordDict[word] = 1
            else:
                wordDict[word] += 1
    return wordDict

def calcAlpha(fileKeyWordDict, bias, weightDict):
    alpha = 0
    for key, value in fileKeyWordDict.items():
        if key in weightDict.keys():
            alpha = alpha + (weightDict[key] * value)
    alpha += bias
    return alpha






def classifyDocument(singleFile, bias, weightDict):
    resultString = ['spam','ham']

    fileKeyWordDict = extractKeyWords(singleFile)

    alpha = calcAlpha(fileKeyWordDict, bias, weightDict)

    if alpha <= 0:
        return resultString[1]
    else:
        return resultString[0]











if __name__ == '__main__':
    storePath = os.getcwd()
    parserObj = argparse.ArgumentParser()
    parserObj.add_argument("path_to_folders", help="Specify the path")
    parserObj.add_argument("output_file_name", help="Specify the output file name")
    firstArg = parserObj.parse_args()

    direcPath = firstArg.path_to_folders
    outputFileName = firstArg.output_file_name
    changeDir(direcPath)
    allFiles = findAllFiles(direcPath)

    modelParams = []
    modelParams = openModel(storePath)


    resultList = []
    os.chdir(storePath)



    bias = modelParams[0]
    weightDict = modelParams[1]
    print(len(modelParams))
    with open(outputFileName,mode='w',encoding='latin1') as fileHandle:
        for singleFile in allFiles:
            strValue = classifyDocument(singleFile, bias, weightDict)
            if(strValue == 'spam'):

                fileHandle.write(strValue + ' ')
            elif(strValue=='ham'):

                fileHandle.write(strValue + ' ')


            fileHandle.write(singleFile + '\n')


