import csv
import random
import pandas as pd

basePath = '../keyLogLineEvaluation/data/'
rawWordsTxtPath = basePath + "rawWords.txt"
processNonPasswordKeyLogPath = basePath + 'nonPasswordLines.txt'
userNameTxtPath =  basePath + 'usernames.txt'
passwordTxtPath =  basePath + 'rockyou.txt'
processPasswordKeyLogPath = basePath + 'passwordLines.txt'
allTestDataCsv = basePath + 'allTestData.csv'
trainingDataCsv = basePath + 'trainingDataCsv.csv'
testDataCsv = basePath + 'testDataCsv.csv'
maxLengthOfTestValue = 0

def createRandomNonPasswordKeyLog(rawDataTxtPath, processDataTxtPath):

    meterpeterDict = {1:" <Back> ", 2 : " <Tab> ", 3: " <Return>"}
    with open(rawDataTxtPath, "r", encoding="utf8") as rawDataTxtFile:
        with open(processDataTxtPath,"w", encoding="utf8") as processDataTxt:
            list = rawDataTxtFile.readlines()
            rowsAdded = 0
            for row in list:
                if(len(row) > 50):

                    firstValue = meterpeterDict[random.randint(1,3)];
                    secondValue = meterpeterDict[random.randint(1,3)];
                    thirdValue = meterpeterDict[random.randint(1,3)];

                    numberOfFirstValue = random.randint(0,3);
                    numberOfSecondValue = random.randint(0,3);
                    numberOfThirdValue = random.randint(0,3);

                    thirdOfRowLength = int(len(row)/3);
                    firstValuePostion = random.randint(0,thirdOfRowLength);
                    secondValuePostion = random.randint(thirdOfRowLength +1,thirdOfRowLength * 2);
                    thirdValuePostion = random.randint(thirdOfRowLength*2+1,thirdOfRowLength * 3);

                    rawDataToBeAddedFirstChunk = row[0:firstValuePostion].strip() + firstValue * numberOfFirstValue + row[firstValuePostion+1:thirdOfRowLength].strip();
                    rawDataToBeAddedSecondChunk = row[thirdOfRowLength+1:secondValuePostion].strip() + secondValue * numberOfSecondValue + row[secondValuePostion+1:thirdOfRowLength*2].strip();
                    rawDataToBeAddedThirdChunk = row[thirdOfRowLength*2+1:thirdValuePostion].strip() + thirdValue * numberOfThirdValue + row[thirdValuePostion+1:len(row)-1].strip() + '\n';
                    rawDataToBeAdded = rawDataToBeAddedFirstChunk + rawDataToBeAddedSecondChunk + rawDataToBeAddedThirdChunk;
                    rowsAdded = rowsAdded + 1
                    processDataTxt.write(rawDataToBeAdded)
                    if(rowsAdded == 16000):
                        break
        processDataTxt.close()
    rawDataTxtFile.close()

def createRandomPasswordKeyLog(userNameTxtPath, passwordTxtPath, rawWordsTxtPath, processPasswordKeyLogPath):
    with open(userNameTxtPath, "r", encoding="utf8") as userNameTxtFile:
        with open(passwordTxtPath,"r", encoding="utf8") as passwordTxtFile:
            with open(rawWordsTxtPath, "r", encoding="utf8") as rawWordsTxtFile:
                with open(processPasswordKeyLogPath,"w", encoding="utf8") as processPasswordKeyLogFile:
                    userNames = userNameTxtFile.readlines()
                    passwords = passwordTxtFile.readlines()
                    rawWords = rawWordsTxtFile.readlines()

                    maxLengthList = [len(userNames), len(passwords)]
                    maxNumberOfTestCases = min(maxLengthList)
                    rowItemsUsed = []


                    for index in range(0,maxNumberOfTestCases-1):
                        meterpeterDict = {1:" <Back> ", 2 : " <Tab> ", 3: " <Return> "}
                        passwordMeterpeterDict = {1:userNames[index].strip()+passwords[index].strip()+ " <Return> "}
                        passwordMeterpeterDict[2] = userNames[index].strip() + " <Tab> " + passwords[index].strip() + " <Return> "
                        passwordMeterpeterDict[3] = userNames[index][0:int(len(userNames[index])/2)].strip() + " <Back> <Back> " + userNames[index][int(len(userNames[index])/2): int(len(userNames[index]))].strip()+ " <Tab> " + passwords[index].strip() + " <Return> "
                        passwordMeterpeterDict[4] = userNames[index].strip()+ " <Tab> " + passwords[index][0:int(len(passwords[index])/2)].strip() + " <Back> <Back> "+ passwords[index][int(len(passwords[index])/2):int(len(passwords[index]))].strip()+ " <Return> "
                        passwordInfirstOrSecondSection = random.randint(0,2)
                        if(len(rawWords[index]) > 50):
                            lengthOfRawWord = int(len(rawWords[index])/3)
                            postionForItem1 = random.randint(0, lengthOfRawWord)
                            postionForItem2 = random.randint(lengthOfRawWord+1,lengthOfRawWord*2)
                            postionForItem3 = random.randint(lengthOfRawWord*2+1,len(rawWords[index]))

                            item1 = ''
                            item2 = ''
                            item3 = ''

                            if(passwordInfirstOrSecondSection==0):
                                item1= str(passwordMeterpeterDict[random.randint(1,4)])
                                item2= str(meterpeterDict[random.randint(1,3)]) * random.randint(0,3)
                                item3= str(meterpeterDict[random.randint(1,3)]) * random.randint(0,3)
                            elif(passwordInfirstOrSecondSection==1):
                                item2= str(passwordMeterpeterDict[random.randint(1,4)])
                                item1= str(meterpeterDict[random.randint(1,3)]) * random.randint(0,3)
                                item3= str(meterpeterDict[random.randint(1,3)]) * random.randint(0,3)
                            elif(passwordInfirstOrSecondSection==2):
                                item3= str(passwordMeterpeterDict[random.randint(1,4)])
                                item1= str(meterpeterDict[random.randint(1,3)]) * random.randint(0,3)
                                item2= str(meterpeterDict[random.randint(1,3)]) * random.randint(0,3)

                            processedPasswordLineChunk1 = rawWords[index][0:postionForItem1].strip() + item1 + rawWords[index][postionForItem1+1: lengthOfRawWord].strip()
                            processedPasswordLineChunk2 = rawWords[index][lengthOfRawWord+1:postionForItem2].strip() + item2 + rawWords[index][postionForItem2+1: lengthOfRawWord*2].strip()
                            processedPasswordLineChunk3 = rawWords[index][lengthOfRawWord*2+1:postionForItem3].strip() + item3 + rawWords[index][postionForItem3+1: len(rawWords[index])].strip() + '\n'
                            processedPasswordLine =  processedPasswordLineChunk1 + processedPasswordLineChunk2 + processedPasswordLineChunk3
                            rowItemsUsed.append(rawWords[index].strip())
                            processPasswordKeyLogFile.write(processedPasswordLine);



                processPasswordKeyLogFile.close()
            rawWordsTxtFile.close()
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
        '''
        if((indexTxtFile % 4 == 0) & (isPasswordEval == 0)):
            writeRowFromTxtToCsv(row, isPasswordEval, writer)
        elif(isPasswordEval == 1):
            writeRowFromTxtToCsv(row, isPasswordEval, writer)
        '''
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

if __name__ == '__main__':
    print('Start Creating Test Data Csv Files')
    createRandomNonPasswordKeyLog(rawWordsTxtPath, processNonPasswordKeyLogPath)
    createRandomPasswordKeyLog(userNameTxtPath, passwordTxtPath, rawWordsTxtPath, processPasswordKeyLogPath)
    maxLengthOfTestValue = determineLargestValue()
    createAllTestDataCsv()
    createCsvFilesForTestingAndTraining()
    print('Complete')




