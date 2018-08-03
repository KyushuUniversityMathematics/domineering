# 2018.07.16 Y.Mizoguchi
#  training AI player for model1
#
import os, sys
os.environ['KERAS_BACKEND'] = 'theano'
import keras as ks
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Reshape
from keras.utils import np_utils
from keras.callbacks import CSVLogger, TensorBoard
from keras.utils.vis_utils import plot_model
from sklearn.datasets import fetch_mldata
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pickle
from countinglib import vretrieve,int2board,boardprint,rotatecheck,transpose,\
                        board2int,turncheck,boardtex,texprint
import random
#
if len(sys.argv)==1:
    epochs = 10
else:
    epochs = int(sys.argv[1])
#
modelname='model2'
print('epochs = ',epochs)
perfectdata='./counting0.csv'
print('input perfectdata = '+perfectdata)
print('modelname = '+modelname)
#
df = pd.read_csv(perfectdata, header=None)
data = df.values.tolist()
#
Xy = list(map(lambda x:[int2board(x[0]),x[1]],data))
X = list(map(lambda x:x[0],Xy))
y = list(map(lambda x:x[1],Xy))
#
Xy_train = Xy
X_train = np.array(list(map(lambda x:np.array(x[0]),Xy_train)))
X_train = X_train.reshape(X_train.shape[0],4,4,1)
X_train = X_train.astype('float32')
y_train = np.array(list(map(lambda x:x[1],Xy_train)))
y_train = np_utils.to_categorical(y_train, 3)
print('X_train.shape,y_train.shape')
print(X_train.shape,y_train.shape)
#
# model1 : Sequential + Dense
#
model = Sequential()
model.add(Conv2D(16, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(4,4,1)))
model.add(Flatten())
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='tanh'))
#
model.add(Dense(3, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
fm='./dump/'+modelname+'.pdf'
print('Saving model flowchart to '+fm)
plot_model(model, to_file=fm, show_shapes=True)
#
callbacks=[]
fh='./dump/'+modelname+"_{0:05d}".format(epochs)+'.csv'
fm='./dump/'+modelname+"_{0:05d}".format(epochs)+'.h5'
#
print('Training (epochs='+str(epochs)+')')
callbacks.append(CSVLogger(fh))
model.fit(X_train, y_train, epochs=epochs, verbose=0, callbacks=callbacks)
#
print('Saving learning logs to '+fh)
print('Saving learned model to '+fm)
model.save(fm)
#
