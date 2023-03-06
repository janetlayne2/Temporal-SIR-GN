import argparse
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import loader
import random

def parse_args():
    parser = argparse.ArgumentParser(description='Directed Temporal SirGN')
    parser.add_argument("--input", type=str, default="Data/synth_0.0.txt",
            help="Input graph path")
    parser.add_argument("--output", type=str, default='emb/synth0emb.txt',
            help="Output embedding path")
    parser.add_argument("--depth", type=int, default=10,
            help="Number of iterations")
    parser.add_argument("--alpha", type=int, default=1,
            help="alpha value. Default = 1")
    parser.add_argument("--clusters", type=int, default=10,
            help="Number of clusters. Default = 10")
    parser.add_argument("--stop", default=False, action = "store_true",
    help="Automatic algorithm stop at convergence. Choose True or False.")

    return parser.parse_args()

# takes G from loader, (n) number of clusters, alpha value, and depth
def dirtemporalSirGN(G,n,alpha,iter=10):
    nv=len(G) 
    embd=np.array([[1/n for i in range(n)] for x in range(nv)])
    emb=dirtemporalAggregation(embd,G,alpha)
    for i in range(iter):
        print(i)
        scaler = MinMaxScaler()
        emb1=scaler.fit_transform(emb)
        kmeans = KMeans(n_clusters=n, random_state=1).fit(emb1)
        val=kmeans.transform(emb1)
        M=val.max(axis=1)
        m=val.min(axis=1)
        subx=(M.reshape(nv,1)-val)/(M-m).reshape(nv,1)
        su=subx.sum(axis=1)
        subx=subx/su.reshape(nv,1)
        emb=dirtemporalAggregation(subx,G,alpha)
    return emb

# takes G from loader, (n) number of clusters, alpha value, and depth
# Stops at convergence or at 100 iterations
def dirtemporalSirGNStop(G,n,alpha,iter=100):
    nv=len(G) 
    embd=np.array([[1/n for i in range(n)] for x in range(nv)])
    emb=dirtemporalAggregation(embd,G,alpha)
    count=getnumber(emb)
    print('count',count)
    for i in range(iter):
        print(i)
        scaler = MinMaxScaler()
        emb1=scaler.fit_transform(emb)
        kmeans = KMeans(n_clusters=n, random_state=1).fit(emb1)
        val=kmeans.transform(emb1)
        M=val.max(axis=1)
        m=val.min(axis=1)
        subx=(M.reshape(nv,1)-val)/(M-m).reshape(nv,1)
        su=subx.sum(axis=1)
        subx=subx/su.reshape(nv,1)
        emb2=dirtemporalAggregation(subx,G,alpha)
        count1=getnumber(emb2)
        print('count',count1)
        if count>=count1:
            break
        else:
            emb=emb2
            count=count1
    return emb

#Temporal aggregation method
def dirtemporalAggregation1(embd,G,v,alpha):
    k=embd.shape[1]
    h=np.zeros((k*2,k*2))
    h1=np.zeros((1,k*2))
    w=[]
    for i in range(len(G[v])):
        #in is first in tuple, out is second
        (ti,lii, lio)=G[v][i]
        wiin=np.zeros((k,))
        wiout=np.zeros((k,))
        for f in lii:
            wiin+=embd[f,:] #sum of all the neighbors at this timestamp
        for g in lio:
            #print('f', f)
            wiout+=embd[g,:] #sum of all the neighbors at this timestamp
        wiboth=np.hstack([wiin, wiout])
        h1+=wiboth #sum of all the neighbors for all timestamps
        w.append(wiboth.reshape((k*2,1)))
    z=np.zeros((1,k*2))
    for i in range(1,len(G[v])):
        (tni,lii, lio)=G[v][i]
        (tnim1,lim1i, lim1o)=G[v][i-1]
        z=np.exp((tni-tnim1)/alpha)*(w[i-1].transpose()+z)
        a=w[i]*z
        h+=a
    g=h.flatten()
    return np.hstack([g.reshape((1,g.shape[0])),h1])



# calls Temporal Aggregation method per node
def dirtemporalAggregation(embd,G,alpha):
    m=[]
    nv=len(G)
    for v in range(nv):
        m.append(dirtemporalAggregation1(embd,G,v,alpha))
    return np.vstack(m)

#returns number of unique node representations for convergence calculation
def getnumber(emb):
    ss=set()
    for x in range(emb.shape[0]):
        sd=''
        for y in range(emb.shape[1]):
            sd+=','+str(emb[x,y])
        ss.add(sd)
    return len(ss)



    
def main(args):
   data = pd.read_csv(args.input)
   l = loader.loader()
   l.read(data)

   if args.stop:
        emb = dirtemporalSirgnStop(l.G, args.clusters, args.alpha)
   else:
        emb = dirtemporalSirgn(l.G, args.clusters, args.alpha, args.depth) 
	
   l.storeEmb(args.output, emb)


if __name__ == "__main__":
    args = parse_args()
    main(args)
