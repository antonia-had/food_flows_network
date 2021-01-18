import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


data = pd.read_csv('erl_14_8_084011_sd_3.csv')
G = nx.from_pandas_edgelist(df=data, source='ori', target='des', edge_attr='total',create_using = nx.DiGraph())
connectivity = list(G.degree())
connectivity_values = [n[1] for n in connectivity]
centrality = nx.betweenness_centrality(G).values()

plt.figure(figsize = (12,8))
plt.plot(centrality, connectivity_values,'ro')
plt.xlabel('Node centrality', fontsize='large')
plt.ylabel('Node connectivity', fontsize='large')
plt.savefig("node_connectivity.png", dpi = 300)
plt.show()


#Get 95th percentile of largest flows
threshold = np.percentile(data['total'], 95)
data = data.loc[(data['total'] > threshold)]

pos_data = pd.read_csv('counties.csv',delimiter=',')

G = nx.from_pandas_edgelist(df=data, source='ori', target='des', edge_attr='total',create_using = nx.DiGraph())

plt.figure(figsize = (12,8))
m = Basemap(projection='merc',llcrnrlon=-160,llcrnrlat=15,urcrnrlon=-60,
urcrnrlat=50, lat_ts=0, resolution='l',suppress_ticks=True)
mx, my = m(pos_data['lon'].values, pos_data['lat'].values)
pos = {}
for count, elem in enumerate(pos_data['nodes']):
     pos[elem] = (mx[count], my[count])
#nx.draw_networkx_nodes(G, pos = pos, nodelist = G.nodes(),node_color = 'black', alpha = 0.8, node_size = 5)
nx.draw_networkx_edges(G, pos = pos, edge_color='blue', alpha=0.1, arrows = False)
m.drawcountries(linewidth = 2)
m.drawstates(linewidth = 0.2)
m.drawcoastlines(linewidth=2)
plt.tight_layout()
plt.savefig("map.png", dpi = 300)
plt.show()
