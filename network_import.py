import networkx as nx
import pandas as pd
import numpy as np
import csv
import networkx.algorithms as alg
import seaborn as sns
sns.set(style="darkgrid", font_scale=1.2)

# Lol I forgot what this was
pd.options.mode.chained_assignment = None  # default='warn'

# Import dataset and clear missing elo values
data = pd.read_csv('chess-data2.csv',low_memory=False)
data['WhiteElo'] = data['WhiteElo'].replace(['?'],0) 
data['BlackElo'] = data['BlackElo'].replace(['?'],0) 


# Change values to float from string
data['WhiteElo'] = data['WhiteElo'].astype(float)

# Create filtered dataset for games in which winner elo > 2000
elo = data[data['WhiteElo'] > 1600]
game_filtered = elo[~elo["Event"].str.contains("https")]



# Creating new dataset with just selected columns
vars = {'Event','Source','Target','Result'}
elo_filtered = game_filtered[vars]

# Creating new column with boolean value for (white = winner). I see how I can make 
# this shorter but I can't be bothered to do it right now.
elo_filtered['weight'] = (elo_filtered['Result'] == '1-0').astype(int)
elo_filtered = elo_filtered.drop(columns=['Result'])
elo_filtered = elo_filtered.reset_index()
elo_filtered = elo_filtered.drop(columns=['index'])

# Create graph and adjacency matrix in NetworkX
g = nx.convert_matrix.from_pandas_edgelist(elo_filtered, source='Source',target='Target',create_using=nx.DiGraph)
g_multi = nx.convert_matrix.from_pandas_edgelist(elo_filtered, source='Source',target='Target',create_using=nx.MultiGraph)


# Different dataframes for different game types
bullet_df = pd.read_csv('Bullet-data.csv',low_memory=False)
class_df = pd.read_csv('Classical-data.csv',low_memory=False)
corr_df = pd.read_csv('Correspondence-data.csv',low_memory=False)
blitz_df = pd.read_csv('Blitz-data.csv',low_memory=False)
tour_df = pd.read_csv('tournament-data.csv',low_memory=False)



# Created dataframe of nodes sorted by degree
degree_sort = sorted(g.degree, key=lambda x: x[1], reverse=True)
degree_sort = pd.DataFrame(degree_sort)
degree_sort.head(10)


# Different graphs for different game types
bullet_g = nx.convert_matrix.from_pandas_edgelist(bullet_df, source='Source',target='Target',create_using=nx.MultiGraph)
blitz_g = nx.convert_matrix.from_pandas_edgelist(blitz_df, source='Source',target='Target',create_using=nx.MultiGraph)
class_g = nx.convert_matrix.from_pandas_edgelist(class_df, source='Source',target='Target',create_using=nx.MultiGraph)
corr_g = nx.convert_matrix.from_pandas_edgelist(corr_df, source='Source',target='Target',create_using=nx.MultiGraph)
tour_g = nx.convert_matrix.from_pandas_edgelist(tour_df, source='Source',target='Target',create_using=nx.MultiGraph)


# Valentin's playground
col_val = elo_filtered[['Source','Target']].values.ravel()
unique_values =  pd.unique(col_val)
win_rate = np.choose(elo_filtered['weight'], [elo_filtered['Source'], elo_filtered['Target']]).value_counts().div(elo_filtered[['Source', 'Target']].stack().value_counts()).fillna(0)

elo_list = pd.read_csv('playerelo.csv')


nx.set_node_attributes(g, elo_list, "elo")

elo_list = elo_list.replace(['?','#N/A'],2000) 


# print("Year assortativity:", nx.attribute_assortativity_coefficient(g,elo))

# print("Modularity by year:", nx_comm.modularity(g, communities))


# rand = open("rand_data.csv", "w+")
# rand = open("rand_data.csv", "a", newline = "")
# writer = csv.writer(rand)


# for x in range(1379):
#     for y in range(x, 1379):
#         edge_weight = rand_adj[x,y]
#         if edge_weight > 0:
#             writer.writerow((x, y, edge_weight))
            
    
degree_sequence = [d for n, d in g.degree()]
config_model = nx.Graph(nx.configuration_model(degree_sequence))

# Create undirected graph to get num triangles
g_udir = nx.convert_matrix.from_pandas_edgelist(elo_filtered, source='Source',target='Target')
nx.set_node_attributes(g_udir, elo_list, "elo")

triangles = nx.triangles(g_udir)

# Fixing the stupid mistake we made 
# nx.readwrite.gexf.write_gexf(g, 'new_adj.gexf')


# #get communities' node lists. Save then in dictionary
# COMMDICT = {}
# def getcommunities(g):
#     print("getting communities ... ")
#     mod_comm = alg.community.modularity_max.greedy_modularity_communities(g)
#     print("sorting communities in dictionary ...")
#     for x in range(len(mod_comm)):
#         COMMDICT[str(x)] = []
#         # community = mod_comm[x]
#         for member in mod_comm[x]:
#             COMMDICT[str(x)].append(member)

#     comm_file = open("node-comms.csv", "w+")
#     commfile = open("node-comms.csv", "a", newline = "")
#     writer = csv.writer(comm_file)
#     writer.writerow(("ID", "Community"))
#     for key in COMMDICT.keys():
#         for player in COMMDICT[key]:
#             writer.writerow((player, key))
#     comm_file.close()

# getcommunities(g)

# Centralities and shit
print()
print('total graph and config model centralities')

average_degree = sum(degree_sequence)/len(degree_sequence)

print(f'average degree of node in graph = {sum(degree_sequence)/len(degree_sequence)}')

print(f'graph transitivity (undirected) = {alg.cluster.transitivity(g_udir)}')
print(f'graph clique number (undirected) = {alg.clique.graph_clique_number(g_udir)}')

print()
print(f'config model transitivity (undirected) = {alg.cluster.transitivity(config_model)}')
print(f'config model clique number (undirected) = {alg.clique.graph_clique_number(config_model)}')

mod_comm = alg.community.modularity_max.greedy_modularity_communities(g)

eig_centrality_udir = pd.DataFrame.from_dict(alg.centrality.eigenvector_centrality(g_udir), orient='index')

# sns.displot(
#   data=eig_centrality,
#   x=0,
#   kind="hist",
#   aspect=1.7,
#   bins=50
# )

close_centrality = pd.DataFrame.from_dict(alg.centrality.closeness_centrality(g), orient='index')

# sns.displot(
#   data=close_centrality,
#   x=0,
#   kind="hist",
#   aspect=1.7,
#   bins=50
# )

betw_centrality = pd.DataFrame.from_dict(alg.centrality.betweenness_centrality(g), orient='index')

# sns.displot(
#   data=betw_centrality,
#   x=0,
#   kind="hist",
#   aspect=1.7,
#   bins=50
# )

print()




# Bullet event centralities
print()
print()
print('bullet graph and config model centralities')
bullet_g_udir = nx.convert_matrix.from_pandas_edgelist(bullet_df, source='Source',target='Target')
bullet_degree_sequence = [d for n, d in bullet_g_udir.degree()]
bullet_config_model = nx.Graph(nx.configuration_model(bullet_degree_sequence))



print(f'average degree of node in bullet graph = {sum(bullet_degree_sequence)/len(bullet_degree_sequence)}')

print(f'bullet graph transitivity (undirected) = {alg.cluster.transitivity(bullet_g_udir)}')

print(f'bullet graph clique number (undirected) = {alg.clique.graph_clique_number(bullet_g_udir)}')

bullet_eig_centrality_udir = pd.DataFrame.from_dict(alg.centrality.eigenvector_centrality(bullet_g_udir), orient='index')

bullet_close_centrality = pd.DataFrame.from_dict(alg.centrality.closeness_centrality(bullet_g_udir), orient='index')

bullet_betw_centrality = pd.DataFrame.from_dict(alg.centrality.betweenness_centrality(bullet_g_udir), orient='index')
print()
print(f'config model transitivity (undirected) = {alg.cluster.transitivity(bullet_config_model)}')
print(f'config model clique number (undirected) = {alg.clique.graph_clique_number(bullet_config_model)}')

print()




# blitz event centralities
print()
print()
print('blitz graph and config model centralities')
blitz_g_udir = nx.convert_matrix.from_pandas_edgelist(blitz_df, source='Source',target='Target')
blitz_degree_sequence = [d for n, d in blitz_g_udir.degree()]
blitz_config_model = nx.Graph(nx.configuration_model(blitz_degree_sequence))


print(f'average degree of node in blitz graph = {sum(blitz_degree_sequence)/len(blitz_degree_sequence)}')

print(f'blitz graph transitivity (undirected) = {alg.cluster.transitivity(blitz_g_udir)}')

print(f'blitz graph clique number (undirected) = {alg.clique.graph_clique_number(blitz_g_udir)}')

blitz_eig_centrality_udir = pd.DataFrame.from_dict(alg.centrality.eigenvector_centrality(blitz_g_udir), orient='index')

blitz_close_centrality = pd.DataFrame.from_dict(alg.centrality.closeness_centrality(blitz_g_udir), orient='index')

blitz_betw_centrality = pd.DataFrame.from_dict(alg.centrality.betweenness_centrality(blitz_g_udir), orient='index')

print()
print(f'config model transitivity (undirected) = {alg.cluster.transitivity(blitz_config_model)}')
print(f'config model clique number (undirected) = {alg.clique.graph_clique_number(blitz_config_model)}')


print()





# classical event centralities
print()
print()
print('classical graph and config model centralities')
classical_g_udir = nx.convert_matrix.from_pandas_edgelist(class_df, source='Source',target='Target')
classical_degree_sequence = [d for n, d in classical_g_udir.degree()]
classical_config_model = nx.Graph(nx.configuration_model(classical_degree_sequence))


print(f'average degree of node in classical graph = {sum(classical_degree_sequence)/len(classical_degree_sequence)}')

print(f'classical graph transitivity (undirected) = {alg.cluster.transitivity(classical_g_udir)}')

print(f'classical graph clique number (undirected) = {alg.clique.graph_clique_number(classical_g_udir)}')

classical_eig_centrality_udir = pd.DataFrame.from_dict(alg.centrality.eigenvector_centrality(classical_g_udir), orient='index')

classical_close_centrality = pd.DataFrame.from_dict(alg.centrality.closeness_centrality(classical_g_udir), orient='index')

classical_betw_centrality = pd.DataFrame.from_dict(alg.centrality.betweenness_centrality(classical_g_udir), orient='index')
print()
print(f'config model transitivity (undirected) = {alg.cluster.transitivity(classical_config_model)}')
print(f'config model clique number (undirected) = {alg.clique.graph_clique_number(classical_config_model)}')

print()




# # correspondence event centralities
# correspondence_degree_sequence = [d for n, d in corr_g.degree()]
# correspondence_g_udir = nx.convert_matrix.from_pandas_edgelist(corr_df, source='Source',target='Target')


# print(f'average degree of node in correspondence graph = {sum(correspondence_degree_sequence)/len(correspondence_degree_sequence)}')

# print(f'correspondence graph transitivity (undirected) = {alg.cluster.transitivity(correspondence_g_udir)}')

# print(f'correspondence graph clique number (undirected) = {alg.clique.graph_clique_number(correspondence_g_udir)}')

# correspondence_eig_centrality_udir = pd.DataFrame.from_dict(alg.centrality.eigenvector_centrality(correspondence_g_udir), orient='index')

# correspondence_close_centrality = pd.DataFrame.from_dict(alg.centrality.closeness_centrality(correspondence_g_udir), orient='index')

# correspondence_betw_centrality = pd.DataFrame.from_dict(alg.centrality.betweenness_centrality(correspondence_g_udir), orient='index')






# tournament event centralities
print()
print()
print('tournament graph and config model centralities')
tour_g_udir = nx.convert_matrix.from_pandas_edgelist(tour_df, source='Source',target='Target')
tour_degree_sequence = [d for n, d in tour_g_udir.degree()]
tour_config_model = nx.Graph(nx.configuration_model(tour_degree_sequence))


print(f'average degree of node in tournament graph = {sum(tour_degree_sequence)/len(tour_degree_sequence)}')

print(f'tournament graph transitivity (undirected) = {alg.cluster.transitivity(tour_g_udir)}')

print(f'tournament graph clique number (undirected) = {alg.clique.graph_clique_number(tour_g_udir)}')

tour_eig_centrality_udir = pd.DataFrame.from_dict(alg.centrality.eigenvector_centrality(tour_g_udir), orient='index')

tour_close_centrality = pd.DataFrame.from_dict(alg.centrality.closeness_centrality(tour_g_udir), orient='index')

tour_betw_centrality = pd.DataFrame.from_dict(alg.centrality.betweenness_centrality(tour_g_udir), orient='index')

print()
print(f'config model transitivity (undirected) = {alg.cluster.transitivity(tour_config_model)}')
print(f'config model clique number (undirected) = {alg.clique.graph_clique_number(tour_config_model)}')