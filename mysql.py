import parfor
import pymysql
import numpy as np


class MySql:
    __host = ""
    __user = ""
    __password = ""
    __db = ""
    __charset = ""

    def __init__(self):
        file = open("init.ini", 'r')
        self.__host = file.readline()[:-1]
        self.__user = file.readline()[:-1]
        self.__password = file.readline()[:-1]
        self.__db = file.readline()[:-1]
        self.__charset = file.readline()[:-1]
        file.close()

    def select(self, coinName, tableType):
        connect = pymysql.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            db=self.__db,
            charset=self.__charset
        )

        if tableType == "min":
            tableName = coinName + "_minute"
        elif tableType == "10min":
            tableName = coinName + "_10minute"
        elif tableType == "30min":
            tableName = coinName + "_30minute"
        elif tableType == "hour":
            tableName = coinName + "_hour"
        elif tableType == "day":
            tableName = coinName + "_day"
        elif tableType == "month":
            tableName = coinName + "_month"
        elif tableType == "year":
            tableName = coinName + "_year"
        else:
            return list()

        try:
            cur = connect.cursor()

            query = "select StartPrice, EndPrice, MaxPrice, MinPrice, TradeAmount from bithumb." + tableName
            cur.execute(query)
            data = [item[:] for item in cur.fetchall()]
            connect.commit()
            connect.close()
            return data

        except Exception as e:
            print(e)
            return list()

    def getTrainData(self, coinName, tableType):
        table = self.select(coinName, tableType)

        maxList = np.max(table, axis=0)
        minList = np.min(table, axis=0)

        maxPrice = maxList[2]
        minPrice = minList[3]
        maxAmount = maxList[4]
        minAmount = minList[4]

        newTable = [[0 for i in range(5)] for j in range(len(table))]

        for i in range(len(table)):
            for j in range(4):
                newTable[i][j] = (table[i][j] - minPrice) / (maxPrice - minPrice)
            newTable[i][4] = (table[i][4] - minAmount) / (maxAmount - minAmount)

        xTrain = [[] for i in range(len(newTable) - 50)]
        yTrain = [0 for i in range(len(newTable) - 50)]

        for i in range(len(newTable) - 50):
            xTrain[i] = newTable[i:i+50]
            yTrain[i] = (newTable[i+50][0] + newTable[i+50][1]) / 2

        return xTrain, yTrain
