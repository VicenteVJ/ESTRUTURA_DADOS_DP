import networkx as nx
import matplotlib.pyplot as plt

# Crie um grafo direcionado vazio
G = nx.DiGraph()

# Adicione 5 vértices
G.add_nodes_from([1, 2, 3, 4, 5])

# Adicione arestas direcionadas
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (2, 5)])

# Desenhe o grafo
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', arrowsize=20)
plt.show()