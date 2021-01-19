import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


data = pd.read_csv('erl_14_8_084011_sd_3.csv')
#Get 95th percentile of largest flows
threshold = np.percentile(data['total'], 95)
data = data.loc[(data['total'] > threshold)]
G = nx.from_pandas_edgelist(df=data, source='ori', target='des', edge_attr='total',create_using = nx.DiGraph())

'''Basic network analysis'''
#Get number of nodes and number of edges
nnodes = G.number_of_nodes()
degrees_in = [d for n, d in G.in_degree()]
degrees_out = [d for n, d in G.out_degree()]
avrg_degree_in = sum(degrees_in) / float(nnodes)
avrg_degree_out = sum(degrees_out) / float(nnodes)

in_values = sorted(set(degrees_in))
in_hist = [degrees_in.count(x) for x in in_values]
out_values = sorted(set(degrees_out))
out_hist = [degrees_out.count(x) for x in out_values]

plt.figure(dpi=300)
plt.plot(in_values,in_hist,'ro-') # in-degree
plt.plot(out_values,out_hist,'bo-') # out-degree
plt.legend(['In-degree','Out-degree'])
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('Food distribution network')
plt.savefig('degree_distribution.png')
plt.close()

plt.figure(dpi=300)
plt.scatter(degrees_in, degrees_out, color='green', alpha=0.2)
plt.plot(np.arange(35),np.arange(35), color='black')
plt.xlabel('In-degree')
plt.ylabel('Out-degree')
plt.title('Food distribution network')
plt.savefig('in_vs_out_degree.png')
plt.close()

nx.is_strongly_connected(G)
nx.is_weakly_connected(G)

'''Network components'''
strong_components = [len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
weak_components = [len(c) for c in sorted(nx.weakly_connected_components(G), key=len, reverse=True)]

plt.figure(dpi=300)
plt.plot(np.arange(len(weak_components)), weak_components, color='blue', linewidth=3)
plt.plot(np.arange(len(strong_components)), strong_components, color='red', linewidth=3)
plt.yscale('log')
#plt.xscale('log')
plt.legend(['Weakly connected components','Strongly connected components'])
plt.xlabel('Component size')
plt.ylabel('Number of components')
plt.title('Components in food distribution network')
plt.savefig('component_distribution.png')
plt.close()

pos_data = pd.read_csv('counties.csv',delimiter=',')

f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (12,8))
m = Basemap(projection='merc',llcrnrlon=-160,llcrnrlat=15,urcrnrlon=-60,
urcrnrlat=50, lat_ts=0, resolution='l',suppress_ticks=True)
mx, my = m(pos_data['lon'].values, pos_data['lat'].values)
pos = {}
for count, elem in enumerate(pos_data['nodes']):
     pos[elem] = (mx[count], my[count])

plt.sca(ax1)
# identify largest connected component
Gcc = sorted(nx.strongly_connected_components(G), key=len, reverse=True)
G0 = G.subgraph(Gcc[0])
nx.draw_networkx_edges(G0, pos = pos, edge_color="r", width=1.0, alpha=0.5, arrows = False)
m.drawcountries(linewidth = 2)
m.drawstates(linewidth = 0.2)
m.drawcoastlines(linewidth=2)
plt.title('Largest strongly connected component')

plt.sca(ax2)
# identify largest connected component
Gcc = sorted(nx.weakly_connected_components(G), key=len, reverse=True)
G0 = G.subgraph(Gcc[0])
nx.draw_networkx_edges(G0, pos = pos, edge_color="r", width=1.0, alpha=0.5, arrows = False)
m.drawcountries(linewidth = 2)
m.drawstates(linewidth = 0.2)
m.drawcoastlines(linewidth=2)
plt.title('Largest weakly connected component')

plt.sca(ax3)
# identify largest connected component
Gcc = sorted(nx.strongly_connected_components(G), key=len, reverse=True)
for i in range(1, len(Gcc)):
     G0 = G.subgraph(Gcc[i])
     nx.draw_networkx_edges(G0, pos = pos, edge_color="blue", width=1.0, alpha=0.5, arrows = False)
m.drawcountries(linewidth = 2)
m.drawstates(linewidth = 0.2)
m.drawcoastlines(linewidth=2)
plt.title('All other strongly connected components')

plt.sca(ax4)
# identify largest connected component
Gcc = sorted(nx.weakly_connected_components(G), key=len, reverse=True)
for i in range(1, len(Gcc)):
     G0 = G.subgraph(Gcc[i])
     nx.draw_networkx_edges(G0, pos = pos, edge_color="blue", width=1.0, alpha=0.5, arrows = False)
m.drawcountries(linewidth = 2)
m.drawstates(linewidth = 0.2)
m.drawcoastlines(linewidth=2)
plt.title('All other weakly connected components')

plt.tight_layout()
plt.savefig("map_components.png", dpi = 300)
plt.close()
