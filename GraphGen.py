import json
import numpy as np
import random
import os

def GenerateGraph(numVerts, density, maxWeight, numGroups=5):
    nodes = [] ; links = []
    #generate nodes
    for x in range(numVerts):
        nodes.append({'group': random.randrange(1, numGroups), 'name': x})
    #generate links
    for x in nodes:
        for y in nodes[x['name']+1:]:
            if np.random.binomial(1, density) == 1:
                w = np.random.randint(maxWeight)
                links.append({'source': x['name'], 'target': y['name'], 'value': w})
    return {'links': links,'nodes': nodes}

def GraphToJSON(data):
    os.remove('static/graph.json')
    with open('static/graph.json','w') as f: json.dump(data,f)
