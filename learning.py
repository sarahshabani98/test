import numpy as np

beta = 0.7

def rho(r,l):     #l:learner  
    return 1/(1+np.exp(-beta*(r-l)))

def learn(arr):
    lx=int(np.shape(arr)[1])
    ly=int(np.shape(arr)[0])
    Q=np.zeros((ly,lx))
    for i in range(lx):
        for j in range(ly):
            c=[]
            c.append(rho(arr[j,i],arr[j,i]))     #0
            c.append(rho(arr[(j-1)%lx,i],arr[j,i]))  #1  up
            c.append(rho(arr[(j+1)%lx,i],arr[j,i]))  #2   down
            c.append(rho(arr[j,(i-1)%ly],arr[j,i]))  #3 left
            c.append(rho(arr[j,(i+1)%ly],arr[j,i]))  #4 right
            c=np.asarray(c)
            c=c/np.sum(c)
            choice=np.random.choice(5,1,p=c)
            Q[j,i]=choice[0]
    return Q    #Q is a matrice which indicates the person our learner will learn from




#
#a=np.random.randint(0,high=25,size=(10,10),dtype='i')
#Z=learn(a)
#            
            
            
            