
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow import keras

allTestDataCsv = '../allTestData.csv'
trainingDataCsv = '../trainingDataCsv.csv'
testDataCsv = '../testDataCsv.csv'
train_data = []
train_labels = []
test_data = []
test_labels = []

def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

def basicClassification():
    class_names = ['english', 'password']

    char_size = 8231

    model = keras.Sequential()
    model.add(keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(keras.layers.Dense(2, activation=tf.nn.softmax))

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=tf.train.AdamOptimizer(), metrics=['accuracy'])

    model.fit(train_data, train_labels, epochs=10, batch_size=100)

    test_loss, test_acc = model.evaluate(test_data, test_labels)
    print('Test accuracy:', test_acc)

    englishList = []
    english = [72,105,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    englishList.append(english)
    englishListNp = np.array(englishList)
    prediction1 = model.predict(englishListNp)

    passwordList = []
    password = [112,97,115,115,119,111,114,100,49,50,51,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    passwordList.append(password)
    passwordListNp = np.array(passwordList)
    prediction2 = model.predict(passwordListNp)


    print(np.argmax(prediction1[0]))
    print(np.argmax(prediction2[0]))

def parseTrainingAndTestingDataFromCsv(pathToCsv):
    dataFromCsv = pd.read_csv(pathToCsv)
    train_data=[]
    for row in dataFromCsv.iterrows():
        temp=[]
        index, data = row
        listWithLabel = data.tolist()
        del listWithLabel[-1]
        temp.append(listWithLabel)
        train_data.append(listWithLabel)

    labels = np.array(dataFromCsv.isPassword.values)
    data = np.array(train_data)
    return data, labels

if __name__ == '__main__':
    print('Start Training Model')

    trainInfo = parseTrainingAndTestingDataFromCsv(trainingDataCsv)
    train_data = trainInfo[0]
    train_labels = trainInfo[1]

    testInfo = parseTrainingAndTestingDataFromCsv(testDataCsv)
    test_data = testInfo[0]
    test_labels = testInfo[1]

    basicClassification()

