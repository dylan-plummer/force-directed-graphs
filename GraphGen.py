import json
import numpy as np
import os

# Styles
#  - "k" : complete graph
#  - "t" : tree
#  - "c" : components

def GenerateGraph(numVerts, density, maxWeight, style):
    nodes = [] ; links = []

    #generate nodes
    for x in range(numVerts):
        nodes.append({'group': 1, 'name': x})

    #generate links
    if style == "k":
        for x in nodes:
            for y in nodes[x['name']+1:]:
                if np.random.binomial(1, density) == 1:
                    w = np.random.randint(maxWeight)
                    links.append({'source': x['name'], 'target': y['name'], 'value': w})

    if style == "t":
        print("t")
        N = nodes
        C = int(len(N)*density*.33)
        print("C: "+str(C))
        r = N[0]
        N = N[1:] ; N.reverse()
        while N != []:
            print(">" + str(N))
            c = np.random.randint(C)+1
            print("c: "+str(c))
            if len(N) <= c:
                for n in N:
                    print(">>end")
                    w = np.random.randint(maxWeight)
                    links.append({'source': n['name'], 'target': r['name'], 'value': w})
                N=[]
            else:

                print("child: "+str(N[:c]))
                children = N[:c]
                N = N[c:]
                print(N)
                print(len(N) - c, len(N))
                p = np.random.randint(len(N)-c,len(N))

                P = N[:p]+N[p+1:]
                for child in children:
                    w = np.random.randint(maxWeight)
                    links.append({'source':child['name'], 'target': child['name'], 'value': w})
            print("L"+str(links))

    return {'links': links,'nodes': nodes}


G = GenerateGraph(30,.5,10,"t")
#print(G)
print("Nodes:"+str(G['nodes']))
print("Links:"+str(G['links']))

def GraphToJSON(data):
    os.remove('graph.json')
    with open('graph.json','w') as f: json.dump(data,f)
