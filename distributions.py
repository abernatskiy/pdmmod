 #!/usr/bin/python

import sys
import os
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from math import*
from scipy.optimize import curve_fit
from routes import *


#kana1=np.array([12,28,16.5,16.6,10.4,4.8,4.6,2.5,1.1,0.4,0])
kana2=np.array([6.6,25.8,18.4,13.1,10.4,9.5,7.0,4.5,2.8,1.1,0.3,0.0,0,0,0])
#kana3=np.array([24.4,38.4,16.8,12.0,4.4,1.1,1.0,0,0,0,0])
#kana4=np.array([5.5,34,13.3,16.7,14.3,6.1,5.4,3.1,1.4,0.5,0])
ding=np.array([72,21,2.6,0.6,0.2,0.1,0,0,0,0,0,0,0,0,0])
kawa=np.array([30,42,12,6.2,3.3,1.8,1.0,0,0,0,0,0,0,0,0])
lengths=np.array(range(1,16))

arrays = [kana2,ding,kawa]
labels = [('Kanavarioti','r','D'),
          ('Ding','c','o'),('Ferris','m','v')]
normarrays = []
aves = []
def func(l,a):
    return a*a*l*(1-a)**(l-1)

#fig = plt.figure(figsize=(16, 12))
plt.clf()
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().subplots_adjust(left=0.15)
fig = plt.figure(1, figsize=(9,6))
ax = fig.add_subplot(111)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


for array,label in zip(arrays,labels):
    x = array/sum(array)
    normarrays.append(x)
    a=sum(x*lengths)
    aves.append(a)                                                                                                                                                                     
    popt, pcov = curve_fit(func, lengths, x)                                                                                                                                           
    yfit = np.array([func(l,popt[0]) for l in lengths])  
    ax.plot(lengths,yfit,c=label[1],linewidth='4')   
    ax.plot(lengths,x,label[2],c=label[1],markersize=18,linewidth='4')                                                                                                     
                                                                                                          

ax.set_yscale('log')
ax.xaxis.set_tick_params(width=1.5)
ax.yaxis.set_tick_params(width=1.5)
print(aves)                                                                                                                                                                            
#plt.legend(fontsize=20)                                                                                                                                                                
#plt.tick_params(axis='both', which='major', labelsize=24)                                                                                                                              
#plt.title('Some chain length distribution from experiment',fontsize=36)
ax.set_xlabel('Chain length',fontsize=26)
ax.set_ylabel('Prevalence in population',fontsize=26)
ax.set_xticks([1,6,11])
ax.set_xticklabels([r"$1",r"$6$",r"$11$"],fontsize = 25)
ax.set_yticks([0.0001,0.01,1])
ax.set_yticklabels(
    [r"$10^{-4}$",r"$10^{-2}$",r"$10^{0}$"],
    fontsize = 25)

ax.get_yaxis().get_major_formatter().labelOnlyBase = False

ax.set_xlim((1,11))
ax.set_ylim((0.0001,1))

plt.savefig('/tmp/some_flory.pdf')



