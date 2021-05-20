import matplotlib.pyplot as plt
import pandas as pd

gm = pd.read_csv('c/gamma_0.91.csv')
gm1 = pd.read_csv('c/gamma_0.92.csv')
gm2 = pd.read_csv('c/gamma_0.93.csv')
gm3 = pd.read_csv('c/gamma_0.94.csv')
gm4 = pd.read_csv('c/gamma_0.95.csv')
gm5 = pd.read_csv('c/gamma_0.96.csv')
gm6 = pd.read_csv('c/gamma_0.97.csv')
gm7 = pd.read_csv('c/gamma_0.98.csv')
gm8 = pd.read_csv('c/gamma_0.99.csv')
gm9 = pd.read_csv('c/gamma_1.0.csv')

lr = pd.read_csv('c/lr_0.001.csv')
lr1 = pd.read_csv('c/lr_0.0015.csv')
lr2 = pd.read_csv('c/lr_0.002.csv')
lr3 = pd.read_csv('c/lr_0.0025.csv')
lr4 = pd.read_csv('c/lr_0.003.csv')
lr5 = pd.read_csv('c/lr_0.0035.csv')
lr6 = pd.read_csv('c/lr_0.004.csv')
lr7 = pd.read_csv('c/lr_0.0045.csv')
lr8 = pd.read_csv('c/lr_0.005.csv')

rs = pd.read_csv('c/replaysize_16.csv')
rs1 = pd.read_csv('c/replaysize_32.csv')
rs2 = pd.read_csv('c/replaysize_64.csv')
rs3 = pd.read_csv('c/replaysize_128.csv')
rs4 = pd.read_csv('c/replaysize_256.csv')
rs5 = pd.read_csv('c/replaysize_512.csv')
rs6 = pd.read_csv('c/replaysize_1024.csv')

bs = pd.read_csv('c/buffersize_128.csv')
bs1 = pd.read_csv('c/buffersize_256.csv')
bs2 = pd.read_csv('c/buffersize_512.csv')
bs3 = pd.read_csv('c/buffersize_1024.csv')
bs4 = pd.read_csv('c/buffersize_2048.csv')
bs5 = pd.read_csv('c/buffersize_4096.csv')

#그래프 비교
plt.plot(lr2['lr_0.002'])
plt.plot(lr4['lr_0.003'])
plt.legend(['lr_0.002', 'lr_0.003'])
plt.ylabel('reward')
plt.title('lr_0.002 & lr_0.003')
plt.show()


#각 그래프
plt.plot(bs5['buffersize_4096'])
plt.title('buffersize_4096')
plt.ylabel('reward')
plt.show()

