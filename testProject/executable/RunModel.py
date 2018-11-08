from tkinter import *
import numpy as np
import tensorflow as tf
from keras.models import model_from_json

def evaluateSingleTxt():

    json_file = open('../model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("../model.h5", by_name=False)
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

root = Tk()

root.title("Determine Passwords")
userInputSingleTxt = Entry(root)
userInputSingleTxt.grid()
Button(root, text="Submit", command=evaluateSingleTxt).grid()
Label(root, text="Results").grid()
resultLabelUserInputSingleTxt = StringVar()
resultValueUserInputSingleTxt = Label(root, textvariable=resultLabelUserInputSingleTxt)
resultValueUserInputSingleTxt.grid()
root.mainloop()


