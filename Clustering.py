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

data = pd.read_csv("NoBeam_Data.csv", header=None)
X_pre = data.iloc[:, 0:20]
#y = data.iloc[:, 20]


X_pre=X_pre.to_numpy()

#y=y.to_numpy()
X=[]
for i in range(len(X_pre)):
    if X_pre[i].max()<7:
        X.append(X_pre[i])

        
x_ax=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]


x = StandardScaler().fit_transform(X)
pca = PCA(n_components=2)

principalComponents = pca.fit_transform(X)
print(len(X))
#tar=pd.DataFrame(data=y, columns=['targets'])
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
#finalDf = pd.concat([principalDf, tar], axis = 1)


# Step 1 and 2 - Choose the number of clusters (k) and select random centroid for each cluster

#number of clusters
K=10

# Select random observation as centroids
Centroids = (principalDf.sample(n=K))
plt.scatter(principalDf["principal component 1"],principalDf["principal component 2"],c='black')
plt.scatter(Centroids["principal component 1"],Centroids["principal component 2"],c='red')
plt.xlabel('principal component 1')
plt.ylabel('principal component 2')
plt.show()

# Step 3 - Assign all the points to the closest cluster centroid
# Step 4 - Recompute centroids of newly formed clusters
# Step 5 - Repeat step 3 and 4

diff = 1
j=0

while(diff!=0):
    XD=principalDf
    i=1
    for index1,row_c in Centroids.iterrows():
        ED=[]
        #print(i)
        for index2,row_d in XD.iterrows():
            d1=(row_c["principal component 1"]-row_d["principal component 1"])**2
            d2=(row_c["principal component 2"]-row_d["principal component 2"])**2
            d=np.sqrt(d1+d2)
            ED.append(d)
        principalDf[i]=ED
        i=i+1

    #print(principalDf)
    C=[]
    for index,row in principalDf.iterrows():
        min_dist=row[1]
        pos=1
        for i in range(K):
            if row[i+1] < min_dist:
                min_dist = row[i+1]
                pos=i+1
        C.append(pos)
    principalDf["Cluster"]=C
    Centroids_new = principalDf.groupby(["Cluster"]).mean()[["principal component 1","principal component 2"]]
    if j == 0:
        diff=1
        j=j+1
    else:
        diff = (Centroids_new['principal component 2'] - Centroids['principal component 2']).sum() + (Centroids_new['principal component 1'] - Centroids['principal component 1']).sum()
        print(diff.sum())
    Centroids = principalDf.groupby(["Cluster"]).mean()[["principal component 2","principal component 1"]]

color=['blue','green','cyan','pink','orange','yellow','black','purple','brown','lightcoral']
for k in range(K):
    data=principalDf[principalDf["Cluster"]==k+1]
    plt.scatter(data["principal component 1"],data["principal component 2"],c=color[k])
plt.scatter(Centroids["principal component 1"],Centroids["principal component 2"],c='red')
plt.xlabel('principal component 1')
plt.ylabel('principal component 2')
plt.show()

chose = input("which color ")
chose=int(chose)
data1=principalDf[principalDf["Cluster"]==chose]
ind=principalDf.index[principalDf["Cluster"]==1].tolist()
for j in range(len(data1)):
    if(X[ind[j]].max()>2.5):
        plt.plot(x_ax,X[ind[j]])
        plt.ylim(0,6)
        plt.show()

principalDf.to_csv('cluster_result.csv')