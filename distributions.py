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
kana2=np.array([6.6,25.8,18.4,13.1,10.4,9.5,7.0,4.5,2.8,1.1,0.3])
#kana3=np.array([24.4,38.4,16.8,12.0,4.4,1.1,1.0,0,0,0,0])
#kana4=np.array([5.5,34,13.3,16.7,14.3,6.1,5.4,3.1,1.4,0.5,0])
ding=np.array([72,21,2.6,0.6,0.2,0.1,0,0,0,0,0])
kawa=np.array([30,42,12,6.2,3.3,1.8,1.0,0,0,0,0])
hud=np.array([])
lengths=np.array(range(1,12))

arrays = [kana2,ding,kawa]
labels = [('Kanavarioti','r'),
          ('Ding','c'),('Ferris','m')]
normarrays = []
aves = []
def func(l,a):
    return a*a*l*(1-a)**(l-1)

fig = plt.figure(figsize=(16, 12))

for array,label in zip(arrays,labels):
    x = array/sum(array)
    normarrays.append(x)
    a=sum(x*lengths)
    aves.append(a)
    popt, pcov = curve_fit(func, lengths, x)
    yfit = np.array([func(l,popt[0]) for l in lengths])
    plt.plot(lengths,x,'o'+label[1],
             markersize=20,linewidth='4',label=label[0]+': <l>='+str("%0.2f" % a))
    plt.plot(lengths,yfit,label[1],linewidth='4',label=label[0]+': Flory fit')
    



    
print(aves)
plt.legend(fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=24)
plt.title('Some chain length distribution from experiment',fontsize=36)
plt.xlabel('Chain length',fontsize=28)
plt.ylabel('Prevalence in population',fontsize=28)
plt.xlim((1,11))
plt.ylim((0.0001,1))
plt.yscale('log')
plt.savefig('/tmp/some_flory.png')

