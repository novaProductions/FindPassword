
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow import keras

allTestDataCsv = '../allTestData.csv'
trainingDataCsv = '../trainingDataCsv.csv'
validationDataCsv = '../validationDataCsv.csv'
testDataCsv = '../testDataCsv.csv'
train_data = []
train_labels = []
validation_data = []
validation_labels = []
test_data = []
test_labels = []

def myExample():


    char_size = 8231

    model = keras.Sequential()
    model.add(keras.layers.Embedding(char_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.summary()
    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    x_val = train_data
    partial_x_train = validation_data

    y_val = train_labels
    partial_y_train = validation_labels
    history = model.fit(partial_x_train,
                        partial_y_train,
                        epochs=120,
                        steps_per_epoch=10,
                        validation_steps=10,
                        validation_data=(x_val, y_val),
                        verbose=1)

    results = model.evaluate(test_data, test_labels)

    print(results)

    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(acc) + 1)

    # "bo" is for "blue dot"
    plt.plot(epochs, loss, 'bo', label='Training loss')
    # b is for "solid blue line"
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()

    history_dict = history.history
    history_dict.keys()

    plt.clf()   # clear figure
    acc_values = history_dict['acc']
    val_acc_values = history_dict['val_acc']

    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()


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

    validationInfo = parseTrainingAndTestingDataFromCsv(validationDataCsv)
    validation_data = validationInfo[0]
    validation_labels = validationInfo[1]

    testInfo = parseTrainingAndTestingDataFromCsv(testDataCsv)
    test_data = testInfo[0]
    test_labels = testInfo[1]

    myExample()
    #createTrainingAndTestData()

