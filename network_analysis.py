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
