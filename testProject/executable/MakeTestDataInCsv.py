import csv
import pandas as pd
import numpy as np

#englishDictDataText = '../englishData.txt'
#englishDictDataText = '../google-10000-english.txt'
englishDictDataText = '../unix-english.txt'
allTestDataDataCsv = '../allTestDataData.csv'
passwordDataText = '../passwordData.txt'
passwordDataText = '../rockyou.txt'
#passwordDataCsv = '../passwordData.csv'
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

    with open(allTestDataDataCsv, 'w', newline='') as csv_file:
        fieldnames = []
        for i in range(0, maxLengthOfTestValue):
            fieldnames.append('fieldValue' + str(i))
        fieldnames.append('isPassword')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writeContentOfCsv(writer, englishDictDataText, 'false')
        writeContentOfCsv(writer, passwordDataText, 'true')
    csv_file.close()

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
    maxLengthOfTestValue = determineLargestValue()
    createNewCsv()

