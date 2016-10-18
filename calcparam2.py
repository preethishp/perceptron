import os
import argparse



if __name__ == '__main__':
    correctlyClassifiedAsSpam = 0
    correctlyClassifiedAsHam = 0
    countClassifiedAsSpam = 0
    countClassifiedAsHam = 0
    countBelongsinSpam = 0
    countBelongsinHam = 0
    with open('per_output.txt', mode='r', encoding='latin1') as fileHandle:
        for line in fileHandle:
            divData = line.split(sep=None,maxsplit=1)
            divData[0] = divData[0] + '.txt'


            if divData[0] == 'ham.txt':
                if divData[0] in divData[1]:
                    correctlyClassifiedAsHam += 1
                    countClassifiedAsHam += 1
                else:
                    countClassifiedAsHam += 1


            if divData[0] == 'spam.txt':
                if divData[0] in divData[1]:
                    correctlyClassifiedAsSpam += 1
                    countClassifiedAsSpam +=1

                else:
                    countClassifiedAsSpam += 1

        #print(correctlyClassifiedAsSpam, correctlyClassifiedAsHam, countClassifiedAsSpam, countClassifiedAsHam)

        parserObj = argparse.ArgumentParser()
        parserObj.add_argument("path_to_folders", help="Specify the path")
        firstArg = parserObj.parse_args()
        direcPath = firstArg.path_to_folders

        os.chdir(direcPath)

        for dirNamePath, dtory, fileNames in os.walk(direcPath):
            listDirSpam = []
            listDirHam = []
            for name in dtory:
                if name == 'ham':
                    os.chdir(os.path.join(dirNamePath, name))

                    listDirHam.extend(os.listdir(os.getcwd()))
                    countBelongsinHam += len(listDirHam)
                if name == 'spam':
                    os.chdir(os.path.join(dirNamePath, name))

                    listDirSpam.extend(os.listdir((os.getcwd())))
                    countBelongsinSpam += len(listDirSpam)
        #print(countBelongsinSpam, countBelongsinHam)

        print('Precision  Recall  F1')
        precisionSpam = correctlyClassifiedAsSpam/countClassifiedAsSpam
        recallSpam = correctlyClassifiedAsSpam/countBelongsinSpam
        f1ScoreSpam = (2 * precisionSpam * recallSpam)/(precisionSpam + recallSpam)
        precisionSpamStr = str(round(precisionSpam, 2))
        recallSpamStr = str(round(recallSpam, 2))
        f1ScoreSpamStr = str(round(f1ScoreSpam, 2))


        precisionHam = correctlyClassifiedAsHam/countClassifiedAsHam
        recallHam = correctlyClassifiedAsHam/countBelongsinHam
        f1ScoreHam = (2*precisionHam*recallHam)/(precisionHam + recallHam)

        precisionHamStr = str(round(precisionHam , 2))
        recallHamStr = str(round(recallHam, 2))
        f1ScoreHamStr = str(round(f1ScoreHam, 2))

        print('Ham ' + ' ' + precisionHamStr + ' ' + recallHamStr + ' ' + f1ScoreHamStr)
        print('Spam' + ' ' + precisionSpamStr + ' ' + recallSpamStr + ' ' + f1ScoreSpamStr)