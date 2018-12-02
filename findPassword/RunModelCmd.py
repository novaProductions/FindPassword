import numpy as np
import tensorflow as tf
from keras.models import model_from_json

basePathSingleWord = 'singleWordEvaluation/data/'
modelH5SingleWord = basePathSingleWord + 'model.h5'
modelJsonSingleWord = basePathSingleWord + 'model.json'

basePathLogLine = 'keyLogLineEvaluation/data/'
modelH5LogLine = basePathLogLine + 'model.h5'
modelJsonLogLine = basePathLogLine + 'model.json'

userInputKeyLogFilePath = input("Please enter path to key log file: ")

print("For calculation option enter WordOnly, LineOnly or skip")
print("WordOnly - Will only evaluate based on each WORD")
print("LineOnly - Will only evaluate based on each LINE")
print("Skip/Default - Will evaluate based on each word AND line")
optionForCalcualtion = input("Please enter calculation option: ")

def evaluateEntireKeyLogFileOnlyLines():
    listOfLinesWithPassword = {}
    with open(userInputKeyLogFilePath,"r", encoding="utf8") as txt_file:
        dataFromTxtFile = txt_file.readlines()
        for index, row in enumerate(dataFromTxtFile):
            if(len(row) > 1):
                prediction = evaluateLogLine(row)
                if(prediction == 1):
                    listOfLinesWithPassword[str(index)] = row
    return listOfLinesWithPassword

def evaluateEntireKeyLogFileOnlySingleWord():
    listOfWordsThatArePasswords = []
    with open(userInputKeyLogFilePath,"r", encoding="utf8") as txt_file:
        dataFromTxtFile = txt_file.readlines()
        for index, row in enumerate(dataFromTxtFile):
            if(len(row) > 1):
                for wordInRow in row.split():
                    prediction = evaluateSingleWord(wordInRow)
                    if(prediction == 1 and wordInRow != "<Back>" and wordInRow != "<Return>" and wordInRow != "<Tab>"):
                        listOfWordsThatArePasswords.append(ItemFromKeyLog(str(index), wordInRow))
    return listOfWordsThatArePasswords

def evaluateSingleWord(strToBeEvaluated):

    json_file = open(modelJsonSingleWord, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(modelH5SingleWord, by_name=False)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=tf.train.AdamOptimizer(), metrics=['accuracy'])
    english = []
    for index, i in enumerate(strToBeEvaluated):
        english.append(ord(i))
    for s in range(len(english),40):
        english.append(0)

    englishList = []
    englishList.append(english)
    englishListNp = np.array(englishList)

    prediction = model.predict(englishListNp)
    return np.argmax(prediction[0])


def evaluateLogLine(logLineToBeEvaluated):
    json_file = open(modelJsonLogLine, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(modelH5LogLine, by_name=False)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=tf.train.AdamOptimizer(), metrics=['accuracy'])
    english = []
    for index, i in enumerate(convertWordsIntoNumbers(logLineToBeEvaluated)):
        english.append(ord(i))
    for s in range(len(english),48):
        english.append(0)
    englishList = []
    englishList.append(english)
    englishListNp = np.array(englishList)

    prediction = model.predict(englishListNp)
    return np.argmax(prediction[0])

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

def printResultsForWordsOnly(listOfPositives):
    for index, i in enumerate(listOfPositives):
        print("Row # " + i.row + "      Text Value: " + i.value)


def printResultsForLineOnly(listOfPositives):
    for index, i in enumerate(listOfPositives):
        print("Row # " + i + "        Line Value: " + listOfPositives[i])

class ItemFromKeyLog():

    def __init__(self,row,value):
        self.row = row
        self.value = value

listOfWordsThatArePasswords = evaluateEntireKeyLogFileOnlySingleWord()
listOfLinesWithPassword = evaluateEntireKeyLogFileOnlyLines()

if(optionForCalcualtion == "WordOnly"):
    printResultsForWordsOnly(evaluateEntireKeyLogFileOnlySingleWord())
elif(optionForCalcualtion == "LineOnly"):
    printResultsForLineOnly(evaluateEntireKeyLogFileOnlyLines())
else:
    for index, i in enumerate(listOfWordsThatArePasswords):
        if(i.row in listOfLinesWithPassword):
            print("Row # " + i.row + "      Text Value: " + i.value + "        Line Value: " + listOfLinesWithPassword[i.row])
