import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
matrix = [(1, 2), (1, 3), (4, 2), (5, 1), (5, 2), (5, 3)]
G.add_edges_from(matrix)

nx.draw(G)
plt.show()
