import networkx as nx
import pandas as pd
import numpy as np
import csv

# Lol I forgot what this was
pd.options.mode.chained_assignment = None  # default='warn'

# Import dataset and clear missing elo values
data = pd.read_csv('chess-data.csv',usecols=[0,2,3,4,7,8],low_memory=False)
data['WhiteElo'] = data['WhiteElo'].replace(['?'],0) 
data['BlackElo'] = data['BlackElo'].replace(['?'],0) 


# Change values to float from string
data['WhiteElo'] = data['WhiteElo'].astype(float)

# Create filtered dataset for games in which winner elo > 2000
elo = data[data['WhiteElo'] > 1600]
game_filtered = elo[~elo["Event"].str.contains("https")]



# Creating new dataset with just selected columns
vars = {'Event','White','Black','Result'}
elo_filtered = game_filtered[vars]

# Creating new column with boolean value for (white = winner). I see how I can make 
# this shorter but I can't be bothered to do it right now.
elo_filtered['weight'] = (elo_filtered['Result'] == '1-0').astype(int)
elo_filtered = elo_filtered.drop(columns=['Result'])
elo_filtered = elo_filtered.reset_index()
elo_filtered = elo_filtered.drop(columns=['index'])

# Create graph and adjacency matrix in NetworkX
g = nx.convert_matrix.from_pandas_edgelist(elo_filtered, source='White',target='Black',create_using=nx.DiGraph)
adj = nx.adjacency_matrix(g)



# Different dataframes for different game types
bullet_df = elo_filtered[elo_filtered["Event"].str.contains('Rated Bullet game')]
blitz_df = elo_filtered[elo_filtered["Event"].str.contains('Rated Blitz game')]
class_df = elo_filtered[elo_filtered["Event"].str.contains('Rated Classical game')]
corr_df = elo_filtered[elo_filtered["Event"].str.contains('Rated Correspondence game')]



# Created dataframe of nodes sorted by degree
degree_sort = sorted(g.degree, key=lambda x: x[1], reverse=True)
degree_sort = pd.DataFrame(degree_sort)
degree_sort.head(10)


# Different graphs for different game types
bullet_g = nx.convert_matrix.from_pandas_edgelist(bullet_df, source='White',target='Black',create_using=nx.DiGraph)
blitz_g = nx.convert_matrix.from_pandas_edgelist(blitz_df, source='White',target='Black',create_using=nx.DiGraph)
class_g = nx.convert_matrix.from_pandas_edgelist(class_df, source='White',target='Black',create_using=nx.DiGraph)
corr_g = nx.convert_matrix.from_pandas_edgelist(corr_df, source='White',target='Black',create_using=nx.DiGraph)



# Write CSV files for Gephi
bullet_df = bullet_df.rename(columns={'White': 'Source', 'Black': 'Target'})
blitz_df = bullet_df.rename(columns={'White': 'Source', 'Black': 'Target'})
class_df = bullet_df.rename(columns={'White': 'Source', 'Black': 'Target'})
corr_df = bullet_df.rename(columns={'White': 'Source', 'Black': 'Target'})


bullet_df[["Source","Target","weight"]].to_csv('bullet.csv', index = False)
blitz_df[["Source","Target","weight"]].to_csv('blitz.csv', index = False)
class_df[["Source","Target","weight"]].to_csv('class.csv', index = False)
corr_df[["Source","Target","weight"]].to_csv('corr.csv', index = False)




# Valentin's playground
col_val = elo_filtered[['White','Black']].values.ravel()
unique_values =  pd.unique(col_val)
win_rate = np.choose(elo_filtered['weight'], [elo_filtered['White'], elo_filtered['Black']]).value_counts().div(elo_filtered[['White', 'Black']].stack().value_counts()).fillna(0)

elo_list = pd.read_csv('playerelo.csv')