import os
import tensorflow


class TensorFlow2:
    name = ""
    __modelAttribute = list()
    __model = 0
    __modelSavePath = ""
    __checkPointPath = ""
    __checkPointDir = ""
    __checkPointCallBack = 0

    def __init__(self, modelName):
        self.name = modelName
        self.__modelSavePath = "model/" + self.name + ".json"
        self.__checkPointPath = "training/" + modelName + "/cp_{epoch:04d}.ckpt"
        self.__checkPointDir = os.path.dirname(self.__checkPointPath)
        self.__checkPointCallBack = tensorflow.keras.callbacks.ModelCheckpoint(
            filepath=self.__checkPointPath,
            save_weights_only=True,
            verbose=1
        )

    def loadModel(self, modelName):
        self.name = modelName
        self.__modelSavePath = "model/" + self.name + ".json"
        self.__checkPointPath = "training/" + modelName + "/cp_{epoch:04d}.ckpt"
        self.__checkPointDir = os.path.dirname(self.__checkPointPath)

        from tensorflow.keras.models import model_from_json
        json_file = open(self.__modelSavePath, "r")
        loaded_model_json = json_file.read()
        json_file.close()

        self.__model = model_from_json(loaded_model_json)
        self.__model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        self.__model.load_weights(tensorflow.train.latest_checkpoint(self.__checkPointDir))

    def createModelAttribute(self, numInput):
        if str(type(numInput)) == "<class 'int'>":
            self.__modelAttribute.append(tensorflow.keras.layers.Flatten(input_dim=numInput))
        else:
            self.__modelAttribute.append(tensorflow.keras.layers.Flatten(input_shape=numInput))

    def addModelLayer(self, numNode, activation):
        self.__modelAttribute.append(tensorflow.keras.layers.Dense(numNode, activation=activation))

    def addModelDropOut(self, degree):
        return self.__modelAttribute.append(tensorflow.keras.layers.Dropout(degree))

    def setModel(self):
        self.__model = tensorflow.keras.models.Sequential(self.__modelAttribute)
        self.__model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        with open(self.__modelSavePath, "w") as json_file:
            json_file.write(self.__model.to_json())

    def fitModel(self, xTrain, yTrain, numEpochs):
        self.__model.save_weights(self.__checkPointPath.format(epoch=0))
        self.__model.fit(
            xTrain,
            yTrain,
            epochs=numEpochs,
            validation_data=(xTrain, yTrain),
            callbacks=[self.__checkPointCallBack]
        )

    def evaluateModel(self, xTest, yTest):
        self.__model.evaluate(xTest,  yTest, verbose=2)