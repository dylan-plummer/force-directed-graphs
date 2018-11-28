import json
import numpy as np
import os

# Styles
#  - "k" : complete graph
#  - "t" : tree
#  - "c" : components

def GenerateGraph(numVerts, density, maxWeight, style, numGroups=5):
    nodes = [] ; links = []

    #generate nodes
    for x in range(numVerts):
        nodes.append({'group': np.random.randint(numGroups), 'name': x})

    #generate links
    if style == "k":
        for x in nodes:
            for y in nodes[x['name']+1:]:
                if np.random.binomial(1, density) == 1:
                    w = np.random.randint(maxWeight)
                    links.append({'source': x['name'], 'target': y['name'], 'value': w})

    if style == "t": #Generate Tree
        print("t")
        N = nodes                       # Temp node array
        C = int(len(N)*density*.33)     # Random MaxChildren
        print("C: "+str(C))
        r = N[0]                        # Set root node
        N = N[1:] ; N.reverse()         # Remove root node from N, reverse N
        print("---------")
        while N != []:
            #print("<N "+str(len(N))+">" + str(N))
            c = np.random.randint(C)+1  # Choose num children
            #print("c: "+str(c))

            if len(N) <= c:
                for n in N:
                    #print(">>end")
                    w = np.random.randint(maxWeight)
                    links.append({'source': n['name'], 'target': r['name'], 'value': w})
                #print(N)
                #print(">>"+str(len(links)))
                N=[]

            else:
                children = N[:c]    # Get children
                N = N[c:]           # Remove children from N
                #print("<Childs "+str(len(children))+">"+str(N[:c]))
                #print("<N "+str(len(N))+">")
                #choose parent, leave parent in N
                pIndex = np.random.randint(len(N))      # Random parent node index
                P = N[pIndex]
                #print("<P>"+str(P))
                for child in children:
                    w = np.random.randint(maxWeight)
                    links.append({'source':child['name'], 'target': P['name'], 'value': w})
            print("L"+str(links))

    return {'links': links,'nodes': nodes}

#GenerateGraph(20,.5,10,"t")





def GraphToJSON(data):
    os.remove('static/graph.json')
    with open('static/graph.json','w') as f: json.dump(data,f)
