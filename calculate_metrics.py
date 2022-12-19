from numpy.ma import zeros
import pandas as pd
import statistics as stat
import scipy.stats as st
import numpy as np

path = "C:/Users/lisam\Dropbox (Flosonics Medical)/Engineering/Signal Processing/Lisa Hofer/metrics_template.xlsx"
df = pd.read_excel(path)


mean_outlier = df['Mean of outlier score']
CV_HR = df['CV HR']

COD_CFT = df['COD cCFT']
COD_SE = df['COD SE']
COD_SP = df['COD SP']
COD_outlier = df['COD outlier']

num_sessions = len(CV_CFT)

metrics = [CV_CFT, CV_SE, CV_SP, mean_outlier, CV_HR, COD_CFT, COD_SE, COD_SP, COD_outlier]
# metrics = ['CV_CFT', 'CV_SE', CV_SP, mean_outlier, CV_HR, COD_CFT, COD_SE, COD_SP, COD_outlier]

## calculate cut offs
probability = 0.5
j = 0
threshold = np.zeros(len(metrics))
print(threshold)


for item in metrics:
    mean = stat.mean(item)
    stdev = stat.stdev(item)
    # fix to normal distribution scipy.stats.norm>>??????
    cut_off = mean
    # print(item.name, cut_off, '\n')
    threshold[j] = cut_off
    j+=1

# print(threshold)
## run through each session with cut off scenarios

for i in range(0,num_sessions):
     # scenario 1: cft+se or cft+sp or se or sp or outlier
    if (CV_CFT[i]>threshold[0] & CV_SE[i]>threshold[1] | CV_CFT[i]>threshold[0] & CV_SP[i]>threshold[2] | CV_SP[i]>threshold[2] | CV_SE[i]>threshold[1] | mean_outlier[i]>threshold[3]):
        print(i)

