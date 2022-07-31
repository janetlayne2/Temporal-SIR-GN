import pandas as pd
import numpy as np
import scipy as sp

class loader:
    
    def __init__(self):
        self.countID=0
        self.G={}
        self.co={}
        self.revco={}
    
    def nodeID(self,x):
        if x not in self.co:
            self.co[x]=self.countID
            self.countID=self.countID+1
            self.revco[self.co[x]]=x
        return self.co[x]
    
    def read(self,df):
        x=df.values
        for a in range(x.shape[0]):
            i=self.nodeID(x[a,0])
            j=self.nodeID(x[a,1])
            self.addEdge((i,j,float(x[a,2])))
        self.fixG()
        
    def storeEmb(self,file,data):
        file1 = open(file, 'w') 
        for a in range(data.shape[0]):
            s=''+str(int(self.revco[a]))
            for b in range(data.shape[1]):
                s+=' '+str(data[a,b])
            file1.write(s+"\n")
        file1.close()
            
    
    def fixG(self):
        for g in range(len(self.G)):
            orderSet=[t for t in self.G[g]]
            orderSet.sort(reverse=True)
            self.G[g]=[(t,np.array([x for x in self.G[g][t]])) for t in orderSet]

    def addEdge(self,s):
        (l1,l2,t)=s
        if l1 not in self.G:
            self.G[l1]={}
        if l2 not in self.G:
            self.G[l2]={}
        if t not in self.G[l1]:
            self.G[l1][t]=set()
        if t not in self.G[l2]:
            self.G[l2][t]=set()   
        self.G[l1][t].add(l2)
        self.G[l2][t].add(l1)
