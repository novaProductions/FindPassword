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

def evaluateSingleWord():

    json_file = open(modelJsonSingleWord, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(modelH5SingleWord, by_name=False)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=tf.train.AdamOptimizer(), metrics=['accuracy'])
    english = []
    for index, i in enumerate(userInputSingleTxt.get()):
        english.append(ord(i))
    for s in range(len(english),40):
        english.append(0)

    englishList = []
    englishList.append(english)
    englishListNp = np.array(englishList)

    prediction1 = model.predict(englishListNp)

    if(np.argmax(prediction1[0]) == 0):
        resultLabelUserInputSingleTxt.set("NOT a password")
    else:
        resultLabelUserInputSingleTxt.set("This is a password")
    root.update()

def evaluateLogLine():
    json_file = open(modelJsonLogLine, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(modelH5LogLine, by_name=False)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=tf.train.AdamOptimizer(), metrics=['accuracy'])
    english = []
    for index, i in enumerate(convertWordsIntoNumbers(userInputLogLine.get())):
        english.append(ord(i))
    for s in range(len(english),53):
        english.append(0)
    englishList = []
    englishList.append(english)
    englishListNp = np.array(englishList)

    prediction1 = model.predict(englishListNp)

    if(np.argmax(prediction1[0]) == 0):
        resultLabelUserInputLogLine.set("Does NOT contain a password")
    else:
        resultLabelUserInputLogLine.set("Does contain password")
    root.update()

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

root = Tk()


root.title("Determine Passwords")
#Validate a single word as password or not
Label(root, text="Enter in single text/phrase to if is a password:").grid(row=0, sticky=W)

userInputSingleTxt = Entry(root)
userInputSingleTxt.grid(row=1,column=0, sticky=W)
Button(root, text="Submit", command=evaluateSingleWord).grid(row=1, column=1, sticky=W)

Label(root, text="Results").grid(row=2, column=0, sticky=W)
resultLabelUserInputSingleTxt = StringVar()
resultValueUserInputSingleTxt = Label(root, textvariable=resultLabelUserInputSingleTxt)
resultValueUserInputSingleTxt.grid(row=2, column=1, sticky=W)

#Validate a single log line if it has a password or not
Label(root, text="Enter in single keylog line to if contains a password:").grid(row=3, sticky=W)

userInputLogLine = Entry(root)
userInputLogLine.grid(row=4,column=0, sticky=W)
Button(root, text="Submit", command=evaluateLogLine).grid(row=4, column=1, sticky=W)

Label(root, text="Results").grid(row=5, column=0, sticky=W)
resultLabelUserInputLogLine = StringVar()
resultValueUserInputLogLine = Label(root, textvariable=resultLabelUserInputLogLine)
resultValueUserInputLogLine.grid(row=5, column=1, sticky=W)

root.mainloop()


