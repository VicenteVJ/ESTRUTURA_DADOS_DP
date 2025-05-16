import networkx as nx
import matplotlib.pyplot as plt

# Crie um grafo vazio
G = nx.Graph()

# Adicione seis vértices
G.add_nodes_from([1, 2, 3, 4, 5, 6])

# Adicione arestas para formar um círculo
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)])

# Desenhe o grafo
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray')
plt.show()