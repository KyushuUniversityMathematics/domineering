# 2018.07.16 Y.Mizoguchi
#  testing AI player for model1
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
    modelname='model1'
    epochs = 10
elif len(sys.argv)==2:
    modelname=sys.argv[1]
    epochs = 10
else:
    modelname=sys.argv[1]
    epochs = int(sys.argv[2])
#
perfectdata='./counting0.csv'
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
no = len(X)
no0 = int(no / 10)
#
Xy_test = random.sample(Xy,no0)
X_test = np.array(list(map(lambda x:np.array(x[0]),Xy_test)))
X_test = X_test.reshape(X_test.shape[0],16)
X_test = X_test.astype('float32')
y_test = np.array(list(map(lambda x:x[1],Xy_test)))
y_test_backup = y_test
y_test = np_utils.to_categorical(y_test, 3)
print('X_test.shape,y_test.shape')
print(X_test.shape,y_test.shape)
#
fp='./dump/'+modelname+"_{0:05d}".format(epochs)+'.h5'
print('Loading model structure from '+fp)
model=load_model(fp)
#
fcsv='./dump/'+modelname+"_{0:05d}".format(epochs)+'.csv'
fpdf='./dump/'+modelname+"_{0:05d}".format(epochs)+'.pdf'
df = pd.read_csv(fcsv)
data = df.values.tolist()
epochs = [x[0] for x in data]
acc =  [x[1] for x in data]
loss = [x[2] for x in data]
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
p1 = ax1.plot(epochs, acc)
p2 = ax1.plot(epochs, loss)
plt.legend((p1[0], p2[0]), ("accuracy", "loss"), loc=3)
plt.title(modelname+' ('+str(epochs)+' epochs learning)')
ax1.set_xlabel('epochs')
ax1.set_ylabel('rate')
ax1.set_ylim(0,1)
ax1.grid(True)
# fig.show()
fig.savefig(fpdf)
print('Saving learning logs graph to '+fpdf)
#
print('Testing...')
loss_and_metrics = model.evaluate(X_test, y_test, batch_size=128)
print('Results: ',loss_and_metrics)


