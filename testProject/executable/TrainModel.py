
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
    tf.set_random_seed(seed)

    # set replace=False, Avoid double sampling
    train_index = np.random.choice(len(X), round(len(X) * 0.8), replace=False)
    test_index = np.array(list(set(range(len(X))) - set(train_index)))
    train_X = X[train_index]
    train_y = y[train_index]
    test_X = X[test_index]
    test_y = y[test_index]

    # Normalized processing, must be placed after the data set segmentation,
    # otherwise the test set will be affected by the training set
    train_X = min_max_normalized(train_X)
    test_X = min_max_normalized(test_X)

    A = tf.Variable(tf.random_normal(shape=[len(allTestData.columns)-1, 1]))
    b = tf.Variable(tf.random_normal(shape=[1, 1]))
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)

    data = tf.placeholder(dtype=tf.float32, shape=[None, len(allTestData.columns)-1])
    target = tf.placeholder(dtype=tf.float32, shape=[None, 1])

    mod = tf.matmul(data, A) + b

    learning_rate = 0.003
    batch_size = 40
    iter_num = 1500
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=mod, labels=target))

    opt = tf.train.GradientDescentOptimizer(learning_rate)
    goal = opt.minimize(loss)

    # Define the accuracy
    # The default threshold is 0.5, rounded off directly
    prediction = tf.round(tf.sigmoid(mod))
    # Bool into float32 type
    correct = tf.cast(tf.equal(prediction, target), dtype=tf.float32)
    # Average
    accuracy = tf.reduce_mean(correct)
    # End of the definition of the model framework

    loss_trace = []
    train_acc = []
    test_acc = []

    for epoch in range(iter_num):
    #Generate random batch index
        batch_index = np.random.choice(len(train_X), size=batch_size)
        batch_train_X = train_X[batch_index]
        batch_train_y = np.matrix(train_y[batch_index]).T
        print(batch_train_X.shape)
        print(batch_train_y.shape)
        sess.run(goal, feed_dict={data: batch_train_X, target: batch_train_y})
        temp_loss = sess.run(loss, feed_dict={data: batch_train_X, target: batch_train_y})
        # convert into a matrix, and the shape of the placeholder to correspond
        temp_train_acc = sess.run(accuracy, feed_dict={data: train_X, target: np.matrix(train_y).T})
        temp_test_acc = sess.run(accuracy, feed_dict={data: test_X, target: np.matrix(test_y).T})
        # recode the result
        loss_trace.append(temp_loss)
        train_acc.append(temp_train_acc)
        test_acc.append(temp_test_acc)
        # output
        if (epoch + 1) % 300 == 0:
            print('epoch: {:4d} loss: {:5f} train_acc: {:5f} test_acc: {:5f}'.format(epoch + 1, temp_loss,
                                                                                     temp_train_acc, temp_test_acc))

# Define the normalized function
def min_max_normalized(data):
    col_max = np.max(data, axis=0)
    col_min = np.min(data, axis=0)
    return np.divide(data - col_min, col_max - col_min)


if __name__ == '__main__':
    print('Start Training Model')
    createTrainingAndTestData()
