import csv
import pandas as pd

#englishDictDataText = '../google-10000-english.txt'
englishDictDataText = '../unix-english.txt'
allTestDataCsv = '../allTestData.csv'
trainingDataCsv = '../trainingDataCsv.csv'
validationDataCsv = '../validationDataCsv.csv'
testDataCsv = '../testDataCsv.csv'
passwordDataText = '../passwordData.txt'
passwordDataText = '../rockyou.txt'
maxLengthOfTestValue = 0

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
    for row in dataFromTxtFile:
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
    notTrainingDataList = []
    validationTrainingDataList = []
    testDataList = []
    for row in allTestData.iterrows():
        index, data = row
        listWithLabel = data.tolist()
        if(index % 2 != 0):
            trainingDataList.append(listWithLabel)
        else:
            notTrainingDataList.append(listWithLabel)
    for index, val in enumerate(notTrainingDataList):
        if(index % 2 != 0):
            validationTrainingDataList.append(val)
        else:
            testDataList.append(val)

    fromListToCvs(trainingDataList, trainingDataCsv)
    fromListToCvs(validationTrainingDataList, validationDataCsv)
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
    maxLengthOfTestValue = determineLargestValue()
    createAllTestDataCsv()
    createCsvFilesForTestingAndTraining()
    print('Complete')




