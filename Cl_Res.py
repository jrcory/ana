import numpy as np 
import scipy 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn import model_selection
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib.patches import Ellipse

##analysis of the results of cluster.py, makes plots of events by cluster 

#set output file 
pdf = PdfPages("cluster.pdf")
##get pca data and split into pca and clusters 
data = pd.read_csv("cluster_result.csv", header=None)
pca = data.iloc[1:-1,1:3]
pca=pca.to_numpy()
#weird hack bc it was not reading it last line 
cl=data.iloc[1:(len(pca)+2),-1]
cl_last=data.iloc[(len(cl)-1),-1]

cl=cl.to_numpy()
cl=[eval(i) for i in cl]

for i in range(len(pca)):
    pca[i][0]=float(pca[i][0])
    pca[i][1]=float(pca[i][1])

#add to one data frame for simplicity 
#this is not the best way to do this 
df1=pd.DataFrame(data=pca,columns=["pc1","pc2"])
df2=pd.DataFrame(data=cl,columns=["Cluster"])
df = pd.concat([df1, df2], axis = 1)

#get data of events and get rid of events 
#make sure this is the same as what was used in cluster.py 
data2 = pd.read_csv("NoBeam_Data.csv", header=None)
X_pre = data2.iloc[:, 0:20]
X_pre=X_pre.to_numpy()
X=[]
for i in range(len(X_pre)):
    if X_pre[i].max()<7:
        X.append(X_pre[i])


#plot the clusters and their colors w/legend 
color=['blue','green','cyan','pink','orange','yellow','black','purple','brown','lightcoral']
h=plt.figure()
for k in range(10):
    d=df[df["Cluster"]==k+1]
    cn=str(k+1)
    plt.scatter(d["pc1"],d["pc2"],c=color[k],label=cn)
plt.xlabel('principal component 1')
plt.ylabel('principal component 2')
plt.legend(loc='upper right')
plt.show()
pdf.savefig(h)

x_ax=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#ask for which cluster I want to look at, hit zero if none 
wcl=input("Which cluster ")

#plots 20 events from that cluster 
plot_lim=20
plt_cnt=0
for i in range(len(pca)-1):
    if cl[i+1]==wcl:
        plt_cnt+=1
        if plt_cnt<plot_lim:
            f=plt.figure(plt_cnt)
            plt.plot(x_ax,X[i])
            ax=plt.gca()
            plt.ylim(-1,6)
            
            f.show()
print(len(X))
print(len(cl))
#could be faster to make pdfs for each cluster 
for j in range(10):
    j=j+1
    print("working on cluster ", j)
    for i in range(len(X)):
        if cl[i]==j:
                g=plt.figure()
                plt.plot(x_ax,X[i]-1)
                plt.ylim(-1.5,6)
                plt.title("Cluster"+str(cl[i]))
                pdf.savefig(g)
                plt.close()
        
pdf.close()
print("done")
input()

