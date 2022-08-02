
import argparse
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import loader
import random

def parse_args():
    parser = argparse.ArgumentParser(description='Temporal SirGN')
    parser.add_argument("--input", type=str, default="Data/synth_0.0.txt",
            help="Input graph path")
    parser.add_argument("--output", type=str, default='emb/synth0emb.txt',
            help="Output embedding path")
    parser.add_argument("--depth", type=int, default=10,
            help="Number of iterations")
    parser.add_argument("--alpha", type=int, default=1,
            help="alpha value. Default = 1")
    parser.add_argument("--clusters", type=int, default=10,
            help="Number of clusters. Final representation will be c^2+c. Default = 10")
    parser.add_argument("--stop", default=False, action = "store_true",
    help="Automatic algorithm stop at convergence. Choose True or False.")

    return parser.parse_args()

# takes G from loader, (n) number of clusters, alpha value, and depth
# returns n^2+n dimensional embedding
def temporalSirgn(G, n, alpha, iter=10):
    nc = len(G) # number of nodes
    emb1=1/n * np.ones((nc, n)) 
    emb = []
    for i in range(nc): 
        emb.append(temporalAgg(emb1, G, i, alpha)) 
    emb = np.vstack(emb)
    for i in range(iter): 
        scaler = MinMaxScaler()
        emb1=scaler.fit_transform(emb)
        kmeans = KMeans(n_clusters=n, random_state=1).fit(emb1)
        val=kmeans.transform(emb1)
        M=val.max(axis=1)
        m=val.min(axis=1)
        subx=(M.reshape(nc,1)-val)/(M-m).reshape(nc,1)
        su=subx.sum(axis=1)
        subx=subx/su.reshape(nc,1)
        emb2 = []
        for j in range(nc):
            emb2.append(temporalAgg(subx, G, j, alpha))
        emb = np.vstack(emb2)    
    return emb 


# takes G from loader, (n) number of clusters, alpha value, and depth
# returns n^2+n dimensional embedding
# Stops at convergence or at 100 iterations
def temporalSirgnStop(G, n, alpha, iter=100):
    nc = len(G) # number of nodes
    emb1=1/n * np.ones((nc, n)) 
    emb = []
    for i in range(nc): 
        emb.append(temporalAgg(emb1, G, i, alpha)) 
    emb = np.vstack(emb)
    count=getnumber(emb)
    for i in range(iter): 
        scaler = MinMaxScaler()
        emb1=scaler.fit_transform(emb)
        kmeans = KMeans(n_clusters=n, random_state=1).fit(emb1)
        val=kmeans.transform(emb1)
        M=val.max(axis=1)
        m=val.min(axis=1)
        subx=(M.reshape(nc,1)-val)/(M-m).reshape(nc,1)
        su=subx.sum(axis=1)
        subx=subx/su.reshape(nc,1)
        emb2 = []
        for j in range(nc):
            emb2.append(temporalAgg(subx, G, j, alpha))
        emb = np.vstack(emb2) 
        count1=getnumber(emb)
        if count>=count1:
            break
        else:
            count=count1   
    return emb


#Temporal aggregation method
def temporalAgg(emb, G, i, alpha):
    s = emb.shape[1]
    M = np.zeros((s, s))
    a = []
    z = np.zeros((1,s))
    e = []
    r = np.zeros((1,s))
    for t in range(len(G[i])):
        (time, neighbors) = G[i][t]
        rep = aggregate(emb, G, i, neighbors, time)
        e.append(rep.reshape((s, 1)))
        r+=rep
    e=np.array(e)
    for t in range(1,len(G[i])) :   
        (ptime, pneighbors)=G[i][t]
        (ltime, lneighbors) = G[i][t-1]
        z=np.exp((ptime-ltime)/alpha)*(e[t-1].transpose()+z)
        a=e[t]*z
        M+=a
    
    M=M.flatten()
    M=np.hstack([M, r[0]])
    return M


# Neighbor Aggregation method
def aggregate(emb, G, i, neighbors, time):
    rep = np.zeros((emb.shape[1],))
    for neigh in neighbors:
        rep+=emb[neigh]
    return rep

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
        emb = temporalSirgnStop(l.G, args.clusters, args.alpha)
   else:
        emb = temporalSirgn(l.G, args.clusters, args.alpha, args.depth) 
	
   l.storeEmb(args.output, emb)


if __name__ == "__main__":
    args = parse_args()
    main(args)


