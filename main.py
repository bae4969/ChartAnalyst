import TF2
import mysql


def makeNewModel(name):
    tfModel = TF2.TensorFlow2("test")
    tfModel.createModelAttribute((50, 5))
    tfModel.addModelLayer(10, 'relu')
    tfModel.addModelDropOut(0.2)
    tfModel.addModelLayer(2, 'softmax')
    tfModel.setModel()

    return tfModel


def loadModel(name):
    tfModel = TF2.TensorFlow2("test")
    tfModel.loadModel(name)

    return tfModel


if __name__ == '__main__':
    sql = mysql.MySql()
    xTrain, yTrain = sql.getTrainData("ada", "min")

    model = loadModel("test")

    model.evaluateModel(xTrain, yTrain)

    # model.load_weights(checkpoint_path)
    # loss,acc = model.evaluate(xTrain,  yTrain, verbose=2)
    # print("복원된 모델의 정확도: {:5.2f}%".format(100*acc))
