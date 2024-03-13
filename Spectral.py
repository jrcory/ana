import numpy as np 
import scipy 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

data = pd.read_csv("Unannotated_Data.csv", header=None)
X = data.iloc[:, 0:20]
#y = data.iloc[:, 20]


X=X.to_numpy()

#data2 = pd.read_csv("notfusion_values.csv")
#xnf = data2.iloc[:, 0:20]

#xnf=xnf.to_numpy()

#size1 = len(xnf)
size2 = len(X)
#if(size1>size2):
    #size=size2
#else:
    #size=size1
size=size2
f_val=[]
nf_val=[]

count = 0
x_ax=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
nf_count=0
pdf = PdfPages("output.pdf")
bad_ev =0
beam_count=0
to_file = np.zeros((2000,21))

for i in range(size):
    

    A=np.fft.fft(X[i])
    p=np.abs(A.imag)**2
    rp=A.real
    
    #print("Fusion maxes ")
    #print(p.max( ))
    f_val.append(p.max())
    n = A.size
    timestep = 0.1
    freq = np.fft.fftfreq(n, d=timestep)
    #plt.plot(freq,A.real,freq,A.imag)
    #plt.title("Fusion FFT")
    #plt.show()
    #plt.plot(freq,A)
    #plt.show()
    #FNF=np.fft.fft(xnf[i])
    #p_nf=np.abs(FNF.imag)**2
    #nf_val.append(p_nf.max())
    #print("Not Fusion Maxes ")
    #print(p_nf.max( ))
    #n2 = FNF.size
    #freq_nf = np.fft.fftfreq(n2, d=timestep)
    #plt.plot(freq_nf,FNF.real,freq_nf,FNF.imag)
    #plt.title("Not Fusion FFT ")
    #plt.show()
    #pmax 15 rp min -5 for non fusion events 
    #pmax > 10 rp min <-10 for fusion
    if X[i].max()>10:
        bad_ev+=1
        continue
    if p.max()<20 and rp.min()>-2.5:
        beam_count+=1
    if count < 1999:
        if beam_count < 1001:
            if(p.max()<20 and rp.min()>-2.5):
                
                fig=plt.figure()
                plt.plot(x_ax,X[i],'-o')
                plt.ylim(0,6)
                plt.title("im max " + str(p.max())+" real min " + str(rp.min()))
                pdf.savefig(fig)
                plt.close()
                fig2=plt.figure()
                plt.plot(freq,A.real,freq,A.imag)
                plt.title("Beam FFT")
                plt.legend(['real','imaginary'])
                pdf.savefig(fig2)
                plt.close()

                to_file[count][0:20]=X[i]
                to_file[count][20]=1
                count+=1
        if(p.max()>35):
            to_file[count][0:20]=X[i]
            to_file[count][20]=0
            count+=1


    

pdf.close()

##editting text, dont want to change file 
#np.savetxt("Annotated_Beam.csv", to_file, delimiter = ",")

#print("Fusion Max and Min ")
#print(max(f_val))
#print(min(f_val))
#print("Not Fusion Max and Min")
#print(max(nf_val))
#print(min(nf_val))
print("Fusion Count ")
print(count)
print("Bad Event Count")
print(bad_ev)
print("Beam Count")
print(beam_count)
