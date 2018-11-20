class WordFromKeyLog():

    def __init__(self,row,value):
        self.row = row
        self.value = value


if __name__ == '__main__':
    print('Start Training Model')

    test = []
    x = WordFromKeyLog(1, "Mike")
    test.append(x)
    print(test[0].value)

