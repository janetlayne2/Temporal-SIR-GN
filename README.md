# Temporal SIR-GN


This repository provides a reference implementation of **Temporal SIR-GN** as described in the paper:

    Temporal SIR-GN: Efficient and Effective Structural Representation Learning for Temporal Graphs

Janet Layne, Justin Carpenter, Edoardo Serra, and Francesco Gullo.

The Temporal SIR-GN algorithm generates structural node representations for an undirected, temporal graph. 

## Usage
From the command line:\s\s
```bash
python temporalSirgn --input filename --output filename --stop False --depth 5 --alpha 10 --clusters 10 
```  

### Input
Temporal SIR-GN takes in a comma separated edgelist in the form of <br>
```bash
node1 node2 timestamp
```

### Output

Output will be a comma separated text file of length *n x (c^2+c)* for a graph with *n* vertices, where *c* is the number of clusters chosen.

## Datasets
All datasets are undirected, but do not have a reverse edge. The preprocessing from loader.py generates an adjacency list with a reverse edge. Datasets are of the form:<br>
```bash
node1 node2 timestamp
```

with labels:<br>
```bash
src trg time
```



