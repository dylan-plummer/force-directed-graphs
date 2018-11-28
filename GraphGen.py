import json
import numpy as np
import os

def GenerateGraph(numVerts, density, maxWeight):
    nodes = [] ; links = []
    #generate nodes
    for x in range(numVerts):
        nodes.append({'group': 1, 'name': x})
    #generate links
    for x in nodes:
        for y in nodes[x['name']+1:]:
            if np.random.binomial(1, density) == 1:
                w = np.random.randint(maxWeight)
                links.append({'source': x['name'], 'target': y['name'], 'value': w})      
    return {'links': links,'nodes': nodes} 

def GraphToJSON(data):
    os.remove('graph.json')
    with open('graph.json','w') as f: json.dump(data,f)