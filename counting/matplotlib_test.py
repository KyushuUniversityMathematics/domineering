# 2018.07.16 Y.Mizoguchi
#  training AI player for model1
#
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pickle
import random
#
modelname='model1'
epochs=10
perfectdata='./counting0.csv'
#
df = pd.read_csv('./dump/model1_00010.csv')
data = df.values.tolist()
epochs = [x[0] for x in data]
acc =  [x[1] for x in data]
loss = [x[2] for x in data]
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(acc,label="acc")
ax1.plot(loss,label="loss")
ax1.set_xlabel('epochs')
ax1.set_ylabel('rate')
ax1.set_ylim(0,1)
ax1.grid(True)
# fig.show()
fig.savefig('model1_00010.pdf')

