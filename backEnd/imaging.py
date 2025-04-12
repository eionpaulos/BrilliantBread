import networkx as nx
import json

# Load the input JSON
with open('inputs.json', 'r') as f:
    data = json.load(f)

G = nx.Graph()

# Add nodes
for comp in data['components']:
    G.add_node(comp['id'], type=comp['type'], position=comp['position'])

# Add edges
for conn in data['connections']:
    G.add_edge(conn['from'], conn['to'])

# Optionally visualize
nx.draw(G, with_labels=True)

