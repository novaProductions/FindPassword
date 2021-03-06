import csv
import random
import pandas as pd

basePath = '../keyLogLineEvaluation/data/'
processNonPasswordKeyLogPath = basePath + 'nonPasswordLines.txt'
userNameTxtPath =  basePath + 'usernames.txt'
passwordTxtPath =  basePath + 'rockyou.txt'
processPasswordKeyLogPath = basePath + 'passwordLines.txt'
allTestDataCsv = basePath + 'allTestData.csv'
trainingDataCsv = basePath + 'trainingDataCsv.csv'
testDataCsv = basePath + 'testDataCsv.csv'
maxLengthOfTestValue = 0

def createRandomNonPasswordKeyLog(processDataTxtPath):

    meterpeterDict = {1:" <Tab> ", 2 : " <Back> ", 3: " <Return>"}
    with open(processDataTxtPath,"w", encoding="utf8") as processDataTxt:
        for index in range(0,414712):
            if(index % 3 == 0):
                processDataTxt.write(convertWordsIntoNumbers("A"*random.randint(5,15) + meterpeterDict[random.randint(2,3)] + "A"*random.randint(5,15) + meterpeterDict[random.randint(1,2)]))
            elif(index % 2 != 0):
                processDataTxt.write(convertWordsIntoNumbers("A"*random.randint(50,100)))
            else:
                firstValue = meterpeterDict[random.randint(1,3)];
                secondValue = meterpeterDict[random.randint(1,3)];
                thirdValue = meterpeterDict[random.randint(1,3)];

                numberOfFirstValue = random.randint(0,1);
                numberOfSecondValue = random.randint(0,2);
                numberOfThirdValue = random.randint(0,1);

                rawDataToBeAddedFirstChunk = "A"*random.randint(0,10) + firstValue * numberOfFirstValue + "A"*random.randint(0,10);
                rawDataToBeAddedSecondChunk = "A"*random.randint(0,10) + secondValue * numberOfSecondValue + "A"*random.randint(0,10);
                rawDataToBeAddedThirdChunk = "A"*random.randint(0,10) + thirdValue * numberOfThirdValue + "A"*random.randint(0,10) ;
                rawDataToBeAdded = rawDataToBeAddedFirstChunk + rawDataToBeAddedSecondChunk + rawDataToBeAddedThirdChunk;

                processDataTxt.write(convertWordsIntoNumbers(rawDataToBeAdded))

    processDataTxt.close()

def createRandomPasswordKeyLog(userNameTxtPath, passwordTxtPath, processPasswordKeyLogPath):
    with open(userNameTxtPath, "r", encoding="utf8") as userNameTxtFile:
        with open(passwordTxtPath,"r", encoding="utf8") as passwordTxtFile:
            with open(processPasswordKeyLogPath,"w", encoding="utf8") as processPasswordKeyLogFile:
                userNames = userNameTxtFile.readlines()
                passwords = passwordTxtFile.readlines()

                maxLengthList = [len(userNames), len(passwords)]
                maxNumberOfTestCases = min(maxLengthList)

                for index in range(0,maxNumberOfTestCases-1):
                    passwordMeterpeterDict = {}
                    passwordMeterpeterDict[0] = userNames[index].strip()+passwords[index].strip()+ " <Return> "
                    passwordMeterpeterDict[1] = "A"*random.randint(0,10) + userNames[index].strip() + " <Tab> " + passwords[index].strip() + " <Return> "
                    passwordMeterpeterDict[2] = "A"*random.randint(0,10) + userNames[index][0:int(len(userNames[index])/2)].strip() + random.randint(1,3) * "<Back> " + userNames[index][int(len(userNames[index])/2): int(len(userNames[index]))].strip()+ " <Tab> " + passwords[index].strip() + " <Return> "
                    passwordMeterpeterDict[3] = "A"*random.randint(0,10) + userNames[index].strip()+ " <Tab> " + passwords[index][0:int(len(passwords[index])/2)].strip() +  random.randint(1,3) * "<Back> "+ passwords[index][int(len(passwords[index])/2):int(len(passwords[index]))].strip()+ " <Return> "
                    passwordMeterpeterDict[4] = convertWordsIntoNumbers(userNames[index].strip() + " <Tab> " + passwords[index].strip() + " <Return> " )

                    processPasswordKeyLogFile.write(convertWordsIntoNumbers(passwordMeterpeterDict[random.randint(0,4)]));

                processPasswordKeyLogFile.close()
        passwordTxtFile.close()
    userNameTxtFile.close()

def createAllTestDataCsv():

    with open(allTestDataCsv, 'w', newline='') as csv_file:
        fieldnames = []
        for i in range(0, maxLengthOfTestValue):
            fieldnames.append('fieldValue' + str(i))
        fieldnames.append('isPassword')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        fromTxtToCsv(writer, processNonPasswordKeyLogPath, 0)
        fromTxtToCsv(writer, processPasswordKeyLogPath, 1)
    csv_file.close()

def fromTxtToCsv(writer, txtFilePath, isPasswordEval):
    with open(txtFilePath,"r", encoding="utf8") as txt_file:
        dataFromTxtFile = txt_file.readlines()
    for indexTxtFile, row in enumerate(dataFromTxtFile):
        writeRowFromTxtToCsv(row, isPasswordEval, writer)

def writeRowFromTxtToCsv(row, isPasswordEval, writer):
    rowString = row.strip()
    rowValues = {}
    for index, i in enumerate(rowString):
        rowValues['fieldValue' + str(index)] = ord(i)
    for s in range(len(rowValues),maxLengthOfTestValue):
        rowValues['fieldValue' + str(s)] = 0
    rowValues['isPassword'] = isPasswordEval
    writer.writerow(rowValues)

def determineLargestValue():
    processNonPasswordKeyLogPathMaxLength = textFileLongestValue(processNonPasswordKeyLogPath)
    processPasswordKeyLogPathMaxLength = textFileLongestValue(processPasswordKeyLogPath)
    maxLengthList = [processNonPasswordKeyLogPathMaxLength, processPasswordKeyLogPathMaxLength]
    return max(maxLengthList)

def textFileLongestValue(txtPath):
    with open(txtPath,"r", encoding="utf8") as txt_file:
        list = txt_file.readlines()
        longestStringLength = 0
        for row in list:
            rowStringLength = len(row.strip())
            if longestStringLength < rowStringLength:
                longestStringLength = rowStringLength
    txt_file.close()
    return longestStringLength

def createCsvFilesForTestingAndTraining():
    allTestData = pd.read_csv(allTestDataCsv)
    trainingDataList =[]
    testDataList = []
    for row in allTestData.iterrows():
        index, data = row
        listWithLabel = data.tolist()
        if(index % 4 != 0):
            trainingDataList.append(listWithLabel)
        else:
            testDataList.append(listWithLabel)

    fromListToCvs(trainingDataList, trainingDataCsv)
    fromListToCvs(testDataList, testDataCsv)

def fromListToCvs(listOfRows, pathToCsv):

    with open(pathToCsv, 'w', newline='') as csv_file:
        fieldnames = []
        for i in range(0, maxLengthOfTestValue):
            fieldnames.append('fieldValue' + str(i))
        fieldnames.append('isPassword')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for rowData in listOfRows:
            rowValues = {}
            for index, i in enumerate(rowData):
                if(index == maxLengthOfTestValue):
                    rowValues['isPassword'] = rowData[index]
                    break
                else:
                    rowValues['fieldValue' + str(index)] = rowData[index]
            writer.writerow(rowValues)
    csv_file.close()

def convertWordsIntoNumbers(originalString):
    newString = ""
    addToString = False
    countTheGap=0
    for i in originalString:

        if i == "<":
            addToString=True
            newString = newString + str(countTheGap)
            countTheGap=0

        if addToString == True:
            newString = newString + i
        else:
            countTheGap = countTheGap+1

        if i == ">":
            addToString=False

    if newString == "":
        newString = str(countTheGap)

    return newString + '\n'

if __name__ == '__main__':
    print('Start Creating Test Data Csv Files')
    createRandomNonPasswordKeyLog(processNonPasswordKeyLogPath)
    createRandomPasswordKeyLog(userNameTxtPath, passwordTxtPath, processPasswordKeyLogPath)
    maxLengthOfTestValue = determineLargestValue()
    createAllTestDataCsv()
    createCsvFilesForTestingAndTraining()
    print('Complete')




