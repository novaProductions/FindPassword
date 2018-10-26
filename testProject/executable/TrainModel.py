
import pandas as pd
import numpy as np
import tensorflow as tf

allTestDataCsv = '../allTestDataData.csv'

def createTrainingAndTestData():
    print('Hi')
    allTestData = pd.read_csv(allTestDataCsv)
    columnHeaders = []
    for i in range(0, len(allTestData.columns)-2):
        columnHeaders.append('fieldValue' + str(i))
    X = allTestData.drop(labels=columnHeaders, axis=1).values
    y = allTestData.isPassword.values

    seed=5
    np.random.seed(seed)
    #tf.set_random_seed(seed)

    # set replace=False, Avoid double sampling
    train_index = np.random.choice(len(X), round(len(X) * 0.8), replace=False)
    test_index = np.array(list(set(range(len(X))) - set(train_index)))
    train_X = X[train_index]
    train_y = y[train_index]
    test_X = X[test_index]
    test_y = y[test_index]

    # Normalized processing, must be placed after the data set segmentation,
    # otherwise the test set will be affected by the training set
    #train_X = min_max_normalized(train_X)
    #test_X = min_max_normalized(test_X)


if __name__ == '__main__':
    print('Start Training Model')
    createTrainingAndTestData()
