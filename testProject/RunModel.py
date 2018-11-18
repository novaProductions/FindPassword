from tkinter import *
import numpy as np
import tensorflow as tf
from keras.models import model_from_json

basePathSingleWord = 'singleWordEvaluation/data/'
modelH5SingleWord = basePathSingleWord + 'model.h5'
modelJsonSingleWord = basePathSingleWord + 'model.json'

basePathLogLine = 'keyLogLineEvaluation/data/'
modelH5LogLine = basePathLogLine + 'model.h5'
modelJsonLogLine = basePathLogLine + 'model.json'

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


def evaluateForSingleWordTest():
    prediction = evaluateSingleWord(userInputSingleTxt.get())
    printForSingleWordTest(prediction)
    root.update()

def printForSingleWordTest(prediction):
    if(prediction == 0):
        resultLabelUserInputSingleTxt.set("NOT a password")
    else:
        resultLabelUserInputSingleTxt.set("This is a password")

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
    for s in range(len(english),53):
        english.append(0)
    englishList = []
    englishList.append(english)
    englishListNp = np.array(englishList)

    prediction = model.predict(englishListNp)
    return np.argmax(prediction[0])

def evaluateForSingleLogLineTest():
    prediction = evaluateLogLine(userInputLogLine.get())
    printForSingleLogLineTest(prediction)
    root.update()

def printForSingleLogLineTest(prediction):
    if(prediction == 0):
        resultLabelUserInputLogLine.set("Does NOT contain a password")
    else:
        resultLabelUserInputLogLine.set("Does contain password")

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

    return newString + '\n'



def evaluateEntireKeyLogFile():
    #evaluateEntireKeyLogFileOnlyLines()
    evaluateEntireKeyLogFileOnlySingleWord()
    root.update()

def evaluateEntireKeyLogFileOnlyLines():
    listOfLinesWithPassword = []
    with open(userInputKeyLogFilePath.get(),"r", encoding="utf8") as txt_file:
        dataFromTxtFile = txt_file.readlines()
        for index, row in enumerate(dataFromTxtFile):
            if(len(row) > 1):
                prediction = evaluateLogLine(row)
                if(prediction == 1):
                    listOfLinesWithPassword.append(ItemFromKeyLog(str(index), row))
    printOutResultsForEntireLogEvaluation(listOfLinesWithPassword, "Line")

def evaluateEntireKeyLogFileOnlySingleWord():
    listOfWordsThatArePasswords = []
    with open(userInputKeyLogFilePath.get(),"r", encoding="utf8") as txt_file:
        dataFromTxtFile = txt_file.readlines()
        for index, row in enumerate(dataFromTxtFile):
            if(len(row) > 1):
                for wordInRow in row.split():
                    prediction = evaluateSingleWord(wordInRow)
                    if(prediction == 1 and wordInRow != "<Back>" and wordInRow != "<Return>" and wordInRow != "<Tab>"):
                        listOfWordsThatArePasswords.append(ItemFromKeyLog(str(index), wordInRow))
    printOutResultsForEntireLogEvaluation(listOfWordsThatArePasswords, "Word")

def printOutResultsForEntireLogEvaluation(listOfPositives, category):
    headerValue = StringVar()
    headerLabel = Label(root, textvariable=headerValue)
    headerLabel.grid(row=9, column=0, sticky=W)
    headerValue.set("Row #     " + category)

    for index, i in enumerate(listOfPositives):
        rowValue = StringVar()
        rowLabel = Label(root, textvariable=rowValue)
        rowLabel.grid(row=10+index, column=0, sticky=W)
        rowValue.set(i.row + "              " + i.value)

class ItemFromKeyLog():

    def __init__(self,row,value):
        self.row = row
        self.value = value

root = Tk()


root.title("Determine Passwords")
#Validate a single word as password or not
Label(root, text="Enter in single text/phrase to if is a password:").grid(row=0, sticky=W)

userInputSingleTxt = Entry(root, width=50)
userInputSingleTxt.grid(row=1,column=0, sticky=W)
Button(root, text="Submit", command=evaluateForSingleWordTest).grid(row=1, column=1, sticky=W)

Label(root, text="Results").grid(row=2, column=0, sticky=W)
resultLabelUserInputSingleTxt = StringVar()
resultValueUserInputSingleTxt = Label(root, textvariable=resultLabelUserInputSingleTxt)
resultValueUserInputSingleTxt.grid(row=2, column=1, sticky=W)

#Validate a single log line if it has a password or not
Label(root, text="Enter in single keylog line to if contains a password:").grid(row=3, sticky=W)

userInputLogLine = Entry(root, width=50)
userInputLogLine.grid(row=4,column=0, sticky=W)
Button(root, text="Submit", command=evaluateForSingleLogLineTest).grid(row=4, column=1, sticky=W)

Label(root, text="Results").grid(row=5, column=0, sticky=W)
resultLabelUserInputLogLine = StringVar()
resultValueUserInputLogLine = Label(root, textvariable=resultLabelUserInputLogLine)
resultValueUserInputLogLine.grid(row=5, column=1, sticky=W)

#Validate entire key log text file
Label(root, text="Enter in path to keylog txt file to see where passwords are:").grid(row=6, sticky=W)

userInputKeyLogFilePath = Entry(root, width=50)
userInputKeyLogFilePath.grid(row=7,column=0, sticky=W)
Button(root, text="Submit", command=evaluateEntireKeyLogFile).grid(row=7, column=1, sticky=W)

Label(root, text="Results").grid(row=8, column=0, sticky=W)
resultLabelKeyLogFile = StringVar()
resultValueKeyLogFile = Label(root, textvariable=resultLabelKeyLogFile)
resultValueKeyLogFile.grid(row=8, column=1, sticky=W)

root.mainloop()


