import matplotlib.pyplot as plt
import networkx as nx

# Create Directed Graph
G = nx.DiGraph()

# Nodes
nodes = {
    'User': {'label': 'User', 'color': 'lightgreen'},
    'Frontend': {'label': 'Frontend Dashboard\n(React.js + D3.js)', 'color': 'lightblue'},
    'API': {'label': 'API Gateway\n(Django + OAuth 2.0)', 'color': 'lightblue'},
    'Detection': {'label': 'Phishing Detection Engine\n(TensorFlow + Kafka)', 'color': 'lightblue'},
    'ThreatDB': {'label': 'Threat Intelligence DB\n(STIX/TAXII)', 'color': 'lightyellow'},
    'Blockchain': {'label': 'Blockchain Evidence Ledger\n(Ethereum/Hyperledger)', 'color': 'lightcoral'},
    'CERT': {'label': 'CERT-In API\n(Takedown Request Submission)', 'color': 'lightpink'},
    'AWS': {'label': 'AWS GovCloud Storage\n(Encrypted Storage)', 'color': 'lightgrey'}
}

# Add nodes
for node, attr in nodes.items():
    G.add_node(node, label=attr['label'], color=attr['color'])

# Edges
edges = [
    ('User', 'Frontend'),
    ('Frontend', 'API'),
    ('API', 'Detection'),
    ('Detection', 'ThreatDB'),
    ('Detection', 'Blockchain'),
    ('Blockchain', 'CERT'),
    ('CERT', 'AWS'),
    ('ThreatDB', 'Detection')
]

G.add_edges_from(edges)

# Node colors
colors = [nodes[node]['color'] for node in G.nodes()]
labels = nx.get_node_attributes(G, 'label')

# Plotting
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, labels=labels, node_color=colors, node_size=3000, font_size=10, font_color='black', edge_color='grey', linewidths=2, arrows=True)

plt.title("Cybersecurity Architecture Diagram")
plt.show()

print("Cybersecurity Architecture Diagram Generated Successfully!")


