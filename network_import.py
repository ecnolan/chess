import networkx as nx
import pandas as pd
import numpy as np

data = pd.read_csv('chess-data.csv',usecols=[0,2,3,4,7],low_memory=False)

# Lol I forgot what this was
pd.options.mode.chained_assignment = None  # default='warn'

# Clear missing elo values
data['WhiteElo'] = data['WhiteElo'].replace(['?'],0)

# Change values to float from string
data['WhiteElo'] = data['WhiteElo'].astype(float)

# Create filtered dataset for games in which winner elo > 2000
elo = data[data['WhiteElo'] > 2000]

# Creating new dataset with just selected columns
vars = {'White','Black','Result'}
elo_filtered = elo[vars]

# Creating new column with boolean value for (white = winner). I see how I can make 
# this shorter but I can't be bothered to do it right now.
elo_filtered['winner_raw'] = elo_filtered['White'] == '1-0'
elo_filtered['winner_raw'] = elo_filtered['winner_raw'].astype(int)
elo_filtered = elo_filtered.drop(columns=['Result'])
elo_filtered = elo_filtered.reset_index()
elo_filtered = elo_filtered.drop(columns=['index'])

weight = elo_filtered['winner_raw']


# Create graph and adjacency matrix in NetworkX
g = nx.convert_matrix.from_pandas_edgelist(elo_filtered, source='White',target='Black',create_using=nx.DiGraph)
adj = nx.adjacency_matrix(g)


