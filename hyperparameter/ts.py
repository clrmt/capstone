import numpy as np
import pandas as pd
import seaborn as sns
from pylab import plot, title, legend, show
from matplotlib import pyplot as plt

dataset = pd.read_csv('csv/learningrate_0.0010.csv') #default

dt1 = pd.read_csv('csv/learningrate_0.0001.csv')
dt2 = pd.read_csv('csv/learningrate_0.0005.csv')
dt3 = pd.read_csv('csv/learningrate_0.0015.csv')
dt4 = pd.read_csv('csv/learningrate_0.0020.csv')
dt5 = pd.read_csv('csv/learningrate_0.0025.csv')
dt6 = pd.read_csv('csv/learningrate_0.0030.csv')
dt7 = pd.read_csv('csv/learningrate_0.0040.csv')  #etc


merge = pd.merge(dataset, dt7)
#print(merge) #결합

"""
########산점도
fig = plt.figure(figsize=(15,5))
ax = fig.add_subplot(1,1,1)
ax.plot(merge.num, merge['sum40'], 'o', label='learning_0.004', c='red')
ax.plot(merge.num, merge['sum10'], 'o', label='learning_0.001', c='blue')
ax.legend(loc='best')
plt.xlabel('episode Number')
plt.ylabel('reward')
plt.title('learningrate_0.004 & default')
plt.show()
plt.close()
"""

"""
############배경 채워진 그래프
plt.fill_between(merge.num, merge['sum10'], color='red', label='learning_0.001', alpha=0.3)
plt.fill_between(merge.num, merge['sum40'], color='green', label='learning_0.004', alpha=0.2)

plt.xlabel('episode Number')
plt.ylabel('reward')
plt.title('learningrate_0.004 & default')
plt.grid()
plt.legend(loc='lower right')
plt.show()
"""


"""
#############그래프
plt.plot(merge.num, merge['sum1'], color='red')
plt.plot(merge.num, merge['sum10'], color='blue')
plt.legend(['learningrate_0.0001','learningrate_0.001'])
plt.xlabel('episode Number')
plt.ylabel('reward')
plt.title('learningrate_0.0001 & default')
plt.show()
plt.close()
"""