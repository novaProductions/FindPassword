
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras

basePath = '../keyLogLineEvaluation/data/'

allTestDataCsv = basePath + 'allTestData.csv'
trainingDataCsv = basePath + 'trainingDataCsv.csv'
testDataCsv = basePath + 'testDataCsv.csv'
modelJson = basePath + 'model.json'
modelH5 = basePath + 'model.h5'
train_data = []
train_labels = []
test_data = []
test_labels = []


def basicClassification():

    model = keras.Sequential()
    model.add(keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(keras.layers.Dense(2, activation=tf.nn.softmax))

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=tf.train.AdamOptimizer(), metrics=['accuracy'])


    model.fit(train_data, train_labels, epochs=5, batch_size=100)

    test_loss, test_acc = model.evaluate(test_data, test_labels)
    print('Test accuracy:', test_acc)

    model_json = model.to_json()
    with open(modelJson, "w") as json_file:
        json_file.write(model_json)

    model.save_weights(modelH5)

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

