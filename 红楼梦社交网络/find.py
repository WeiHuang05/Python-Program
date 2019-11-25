import pandas as pd
from pyecharts.charts import Graph
from pyecharts import options as opts
import matplotlib.pyplot as plt
import networkx as nx
import community    # python-louvain
from collections import defaultdict


def draw_graph(G,alpha,node_scale,figsize):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=figsize)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,node_size=[G.degree[x]*node_scale for x in G.nodes])
    nx.draw_networkx_edges(G,pos,alpha=alpha)
    nx.draw_networkx_labels(G,pos)
    plt.axis("off")
    plt.show()


relationship_data = pd.read_csv('relationship.csv')
namenode_data = pd.read_csv('NameNode.csv')
relationship_data_list = relationship_data.values.tolist()
namenode_data_list = namenode_data.values.tolist()


G = nx.Graph()
for link in relationship_data_list:
    G.add_edge(link[0], link[1], weight=link[2])


# 重要人物网络
important_nodes = [node for node in G.nodes if G.degree[node]>=50]
print (important_nodes)
G_sub = G.subgraph(important_nodes).copy()
draw_graph(G_sub,alpha=0.5,node_scale=30,figsize=(6,4))

#最重要人物
page_ranks = pd.Series(nx.algorithms.pagerank(G)).sort_values()
page_ranks.tail(20).plot(kind="barh")
plt.show()

#最有权的人
between = pd.Series(nx.betweenness_centrality(G)).sort_values()
between.tail(20).plot(kind="barh")
plt.show()

#集团发现
important_nodes = [node for node in G.nodes if G.degree[node]>=15]
G_main = G.subgraph(important_nodes).copy()
partition = community.best_partition(G_main)         # Louvain算法划分社区

comm_dict = defaultdict(list)
for person in partition:
    comm_dict[partition[person]].append(person)

def draw_community(comm):
    G_comm = G_main.subgraph(comm_dict[comm]).copy()
    draw_graph(G_comm,alpha=0.2,node_scale=10,figsize=(8,6))
    print("community {}: {}".format(str(comm)," ".join(reversed(sorted(comm_dict[comm],key=G.degree)))))

draw_community(0)  
draw_community(1)  
draw_community(2)
draw_community(3)       
