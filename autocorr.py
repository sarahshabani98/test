import numpy as np


def allele(arr,a,b):
    a_size=np.size(np.where(arr==a))
    b_size=np.size(np.where(arr==b))
    return [a_size,b_size]

def autocorelate(arr1):
    n=np.correlate(arr1,arr1,mode='full')
    N=n[np.size(n)//2:]/np.max(n)
    for i in N:
        if i <= 1/np.exp(1):
            Z=i
            break
    return Z
    
    
    
    