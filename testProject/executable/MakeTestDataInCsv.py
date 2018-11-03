import csv
import pandas as pd

#englishDictDataText = '../google-10000-english.txt'
englishDictDataText = '../unix-english.txt'
allTestDataCsv = '../allTestDataData.csv'
trainingDataCsv = '../trainingDataCsv.csv'
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

def createNewCsv():

    with open(allTestDataCsv, 'w', newline='') as csv_file:
        fieldnames = []
        for i in range(0, maxLengthOfTestValue):
            fieldnames.append('fieldValue' + str(i))
        fieldnames.append('isPassword')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writeContentOfCsv(writer, englishDictDataText, 0)
        writeContentOfCsv(writer, passwordDataText, 1)
    csv_file.close()

def populateCsv():
    allTestData = pd.read_csv(allTestDataCsv)
    dict =[]
    notDict = []
    notDict1 = []
    notDict2 = []
    for row in allTestData.iterrows():
        index, data = row
        listWithLabel = data.tolist()
        if(index % 2 != 0):
            dict.append(listWithLabel)
        else:
            notDict.append(listWithLabel)
    for index, val in enumerate(notDict):
        if(index % 2 != 0):
            notDict1.append(val)
        else:
            notDict2.append(val)

    with open(trainingDataCsv, 'w', newline='') as csv_file:
        fieldnames = []
        for i in range(0, maxLengthOfTestValue):
            fieldnames.append('fieldValue' + str(i))
        fieldnames.append('isPassword')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        #print(listWithLabel)
        for index, i in enumerate(dict):
            #print(listWithLabel[index])
            rowValues = {}
            if(len(i)-2 != index):
                rowValues['fieldValue' + str(index)] = i[index]
            else:
                rowValues['isPassword'] = str(i[index])
                break
        writer.writerow(rowValues)
    csv_file.close()
    print(len(dict))
    print(len(notDict1))
    print(len(notDict2))


def writeContentOfCsv(writer, txtFilePath, isPasswordEval):
    with open(txtFilePath,"r", encoding="utf8") as txt_file:
        list = txt_file.readlines()
    for row in list:
        rowString = row.strip()
        rowValues = {}
        for index, i in enumerate(rowString):
            rowValues['fieldValue' + str(index)] = ord(i)
        for s in range(len(rowValues),maxLengthOfTestValue):
            rowValues['fieldValue' + str(s)] = 0
        rowValues['isPassword'] = isPasswordEval
        writer.writerow(rowValues)

if __name__ == '__main__':
    print('Start Creating Test Data')
    maxLengthOfTestValue = determineLargestValue()
    #createNewCsv()
    populateCsv()
    print('Complete')
