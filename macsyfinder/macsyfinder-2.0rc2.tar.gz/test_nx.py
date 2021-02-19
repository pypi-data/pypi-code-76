import networkx as nx
import matplotlib.pyplot as plt

# https://fr.wikipedia.org/wiki/Clique_(th%C3%A9orie_des_graphes)#Probl%C3%A8me_de_la_clique
# https://en.wikipedia.org/wiki/Clique_problem

class System:
    def __init__(self, id, score):
        self.id = id
        self.score = score

    def __str__(self):
        return f"{self.id}, {self.score:.1f}"

a = System('A', 1.5)
b = System('B', 2.0)
c = System('C', 3.0)
d = System('D', 1.5)
e = System('E', 0.5)
f = System('F', 1.0)
g = System('G', 3.0)
h = System('H', 1.5)

G1 = nx.Graph()
G1.add_nodes_from([a, b, c, d])
G1.add_edge(a, b)
G1.add_edge(b, d)
G1.add_edge(c, d)

G2 = nx.Graph()
G2.add_nodes_from([a, b, c])
G2.add_edge(a, b)

G3 = nx.Graph()
G3.add_nodes_from([b, c, e])
G3.add_edge(b, e)

G4 = nx.Graph()
G4.add_nodes_from([a, b, c, d, e])
G4.add_edge(a, b)
G4.add_edge(b, d)
G4.add_edge(b, e)
G4.add_edge(c, d)
G4.add_edge(d, e)

G5 = nx.Graph()
G5.add_nodes_from([a, b, c, d, e, f])
G5.add_edge(a, b)
G5.add_edge(a, f)
G5.add_edge(b, d)
G5.add_edge(b, e)
G5.add_edge(b, f)
G5.add_edge(c, d)
G5.add_edge(c, f)
G5.add_edge(d, e)
G5.add_edge(e, f)


G6 = nx.Graph()
G6.add_nodes_from([a, b, c, d, g, h])
G6.add_edge(a, b)
G6.add_edge(b, d)
G6.add_edge(b, h)
G6.add_edge(c, d)
G6.add_edge(c, h)
G6.add_edge(d, g)
G6.add_edge(g, h)

g_opts = {'with_labels': True, 'node_size': 500}

fig = plt.figure()
#ax1 = fig.add_subplot(adjustable='box', autoscale_on=True, frame_on=True)
nx.draw_shell(G1, node_color='LightBlue', **g_opts)
plt.savefig('graph_1.png')
#plt.show()

fig = plt.figure()
# ax2 = fig.add_subplot(gs[0, 1], adjustable='box', autoscale_on=True, frame_on=True)
nx.draw_shell(G2, node_color='LightGreen', **g_opts)
plt.savefig('graph_2.png')
#plt.show()

fig = plt.figure()
# ax3 = fig.add_subplot(gs[0, 2], adjustable='box', autoscale_on=True, frame_on=True)
nx.draw_shell(G3, node_color='yellow', **g_opts)
plt.savefig('graph_3.png')
#plt.show()

fig = plt.figure()
# ax4 = fig.add_subplot(gs[1, 0], adjustable='box', autoscale_on=True, frame_on=True)
nx.draw_shell(G4, node_color='orange', **g_opts)
plt.savefig('graph_4.png')
#plt.show()

fig = plt.figure()
# ax5 = fig.add_subplot(gs[1, 1], adjustable='box', autoscale_on=True, frame_on=True)
nx.draw_shell(G5, node_color='pink', **g_opts)
plt.savefig('graph_5.png')
#plt.show()

fig = plt.figure()
# ax6 = fig.add_subplot(gs[1, 2], adjustable='box', autoscale_on=True, frame_on=True)
nx.draw_shell(G6, node_color='turquoise', **g_opts)
plt.savefig('graph_6.png')
#plt.show()

# plt.tight_layout()
# plt.show()

for i, G in enumerate((G1, G2, G3, G4, G5, G6), 1):
    print("\n========= Graph", i)
    cliques = nx.algorithms.clique.find_cliques(G)
    cliques = list(cliques)
    cliques.sort(key=lambda c: sum([s.score for s in c]), reverse=True)
    for c in cliques:
        print([(s.id, s.score) for s in c], f"score= {sum([s.score for s in c])}")
