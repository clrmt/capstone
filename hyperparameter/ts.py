import numpy as np
import pandas as pd
import seaborn as sns
from pylab import plot, title, legend, show
from matplotlib import pyplot as plt

dataset = pd.read_csv('csv/learningrate_0.0010.csv') #default
dataset1 = pd.read_csv('csv/learningrate_0.0040.csv')
dataset2 = pd.read_csv('csv/learningrate_0.0020.csv')
dataset3 = pd.read_csv('csv/learningrate_0.0025.csv')
dataset4 = pd.read_csv('csv/learningrate_0.0030.csv') #etc

merge = pd.merge(dataset4,dataset3)
#print(merge)

########산점도
"""fig = plt.figure(figsize=(15,5))
ax = fig.add_subplot(1,1,1)
ax.plot(merge.num, merge['sum10'], 'o', label='learning_0.001', c='red')
ax.plot(merge.num, merge['sum30'], 'o', label='learning_0.030', c='blue')
#ax.legend(loc='best')
plt.show()
plt.close()"""

############배경 채워진 그래프
"""plt.fill_between(merge.num, merge['sum40'], color='red', label='learning_0.0040' , alpha=0.1)
plt.fill_between(merge.num, merge['sum25'], color='green', label='learning_0.0025', alpha=0.2)

plt.xlabel('episode Number')
plt.ylabel('reward')
plt.title('learningrate_0.001 & 0.0025')
plt.grid()
plt.legend(loc = 'lower right')
plt.show()"""

#############그래프
plt.plot(merge.num, merge['sum30'], color='red')
plt.plot(merge.num, merge['sum25'], color='blue')
plt.legend(['learningrate_0.0030','learningrate_0.025'])
plt.show()
plt.close()
