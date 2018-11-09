import csv
import pandas as pd
import random

basePath = '../singleWordEvaluation/data/'
englishDictDataText = basePath + 'unix-english.txt'
allTestDataCsv = basePath + 'allTestData.csv'
trainingDataCsv = basePath + 'trainingDataCsv.csv'
validationDataCsv = basePath + 'validationDataCsv.csv'
testDataCsv = basePath + 'testDataCsv.csv'
passwordDataText = basePath + 'rockyou.txt'
maxLengthOfTestValue = 0

basePath = '../keyLogLineEvaluation/data/'
rawWordsTxtPath = basePath + "rawWords.txt"
processDataTxtPath = basePath + 'nonPasswordLines.txt'

def determineLargestValue():
    passwordDataMaxLength = textFileLongestValue(passwordDataText)
    englishDictDataMaxLength = textFileLongestValue(englishDictDataText)
    maxLengthList = [passwordDataMaxLength, englishDictDataMaxLength]
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

def createAllTestDataCsv():

    with open(allTestDataCsv, 'w', newline='') as csv_file:
        fieldnames = []
        for i in range(0, maxLengthOfTestValue):
            fieldnames.append('fieldValue' + str(i))
        fieldnames.append('isPassword')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        fromTxtToCsv(writer, englishDictDataText, 0)
        fromTxtToCsv(writer, passwordDataText, 1)
    csv_file.close()

def fromTxtToCsv(writer, txtFilePath, isPasswordEval):
    with open(txtFilePath,"r", encoding="utf8") as txt_file:
        dataFromTxtFile = txt_file.readlines()
    for indexTxtFile, row in enumerate(dataFromTxtFile):
        if((indexTxtFile % 4 == 0) & (isPasswordEval == 1)):
            writeRowFromTxtToCsv(row, isPasswordEval, writer)
        elif(isPasswordEval == 0):
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

def createRandomNonPasswordKeyLog(rawDataTxtPath, processDataTxtPath):
    with open(rawDataTxtPath, "r", encoding="utf8") as txt_file:
        with open(processDataTxtPath,"w", encoding="utf8") as processDataTxt:
            rowItemsUsed = []
            list = txt_file.readlines()
            for row in list:
                additonalRandomPhrase = ''
                if(len(rowItemsUsed) > 10):
                    additonalRandomPhrase = rowItemsUsed[random.randint(0, len(rowItemsUsed)-1)]
                if(len(row) > 50):
                    rowItemsUsed.append(row)
                    processDataTxt.write(row + additonalRandomPhrase.rstrip())
        processDataTxt.close()
    txt_file.close()





if __name__ == '__main__':
    print('Start Creating Test Data Csv Files')
    createRandomNonPasswordKeyLog(rawWordsTxtPath, processDataTxtPath)
    print('Complete')




