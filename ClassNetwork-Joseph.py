"""
Finds the adjacency matrix A, A^3, and self loops in A^4.
Also calculates the graph Laplacian and its eigenvalues.
Can calculate some cut set stats.
"""

import networkx as nx
from networkx.algorithms import bipartite
import networkx.algorithms.community as nx_comm
from networkx.algorithms import bipartite


import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns

import pandas as pd
import numpy as np
import scipy.sparse as sp
from collections.abc import Iterable
from itertools import combinations


# returns an array of the diagonals of a matrix
def find_diag(array):
    array = array.toarray()
    diags = []

    for row in range(len(array)):
        for col in range(len(array[row])):
            if row == col:
                diags.append(array[row][col])

    return diags

def find_cut_sets(graph):
    node_cuts = []
    edge_cuts = []
    comb = combinations(graph.nodes, 2)

    for pair in list(comb):
        node_cuts.append(len(nx.algorithms.connectivity.cuts.minimum_node_cut(graph, pair[0], pair[1])))
        edge_cuts.append(len(nx.algorithms.connectivity.cuts.minimum_edge_cut(graph, pair[0], pair[1])))

    avg_node_cut_len = sum(node_cuts) / len(node_cuts)
    avg_edge_cut_len = sum(edge_cuts) / len(edge_cuts)

    return avg_node_cut_len, avg_edge_cut_len

def get_degrees(graph):
    print(graph.degree())
    degrees = []
    for pair in graph.degree():
        degrees.append(pair[1])
    print(degrees)
    nodes = graph.number_of_nodes()
    for i in range(nodes):
        for j in range(nodes):
            print(i, ", ", j, " degree: ", degrees[i], degrees[j] )

# Takes a scipy sparse array and prints for Overleaf bmatrix formatting
def print_array(sparse_array, file_obj=None, dense=False, numpy="False"):
    if dense == False:
        if numpy == "False":
            array = sparse_array.toarray()
        else:
            array = sparse_array.tolist()
    else:
        array = sparse_array

    syntax = ""
    for row in array:
        if isinstance(row, Iterable):
            for cell in row:
                fill = "     "
                syntax += str(cell) + fill[len(str(cell))]
            syntax += "\n"
        else:
            syntax += str(round(row, 5)) + "\n"

    if file_obj:
        print(syntax, file=file_obj)
    else:
        print(syntax)


# Collect data
adjacency_data = pd.read_csv("./Network Adjacency List.csv")
student_data = pd.read_csv("./Student Degrees.csv")
class_data = pd.read_csv("./Class Degrees.csv")

students = []
classes = []

# List of student Ids
for student in student_data["Id"]:
    students.append(student)

# List of class Ids
# for course in class_data["Id"]:
#     classes.append(course)


# Create graph
bipartite_graph = nx.from_pandas_edgelist(adjacency_data, source="Student", target="Class")


#Sets students as partite 0 and classes as partite 1
nx.set_node_attributes(bipartite_graph, 1, "bipartite")
for id in students:
    bipartite_graph.nodes[id]["bipartite"] = 0


# Create student and class projections
student_nodes = {n for n, d in bipartite_graph.nodes(data=True) if d["bipartite"] == 0}
class_nodes = set(bipartite_graph) - student_nodes

student_graph = bipartite.projected_graph(bipartite_graph, student_nodes)

class_graph = bipartite.projected_graph(bipartite_graph, class_nodes)


# josephs stuff =======================================================================================

# print("Degree assortativity coefficient:", nx.degree_assortativity_coefficient(student_graph))

communities = [{"Reading", "Knollmeyer", "Ross", "Young", "Golden", "Miller", "Wheeler", "Dodes", "Mosbarger"},
                {"Projansky", "Napier Smith", "Bedward"},
                {"Molnar", "Sisk", "Feldman", "Banks", "Komissar", "Nolan", "Nguyen", "Sognamillo", "Wintermute"},
                {"Adair"}]

class_dict = {}
for name in communities[0]:
    class_dict[name] = 2020
for name in communities[1]:
    class_dict[name] = 2021
for name in communities[2]:
    class_dict[name] = 2022
for name in communities[3]:
    class_dict[name] = 2023

nx.set_node_attributes(student_graph, class_dict, "year")

get_degrees(student_graph)


# print("k components: ", nx.k_components(student_graph))

# print("clique number: ", nx.graph_clique_number(student_graph))
#
# print("maximum clique: ", nx.max_clique(student_graph))

# print("node redundancy: ", bipartite.node_redundancy(student_graph))

# print(" average clustering: ", nx.average_clustering(student_graph))

# print(" local clustering: ", nx.clustering(student_graph))

# print("Year assortativity:", nx.attribute_assortativity_coefficient(student_graph, "year"))

# print("Modularity by year:", nx_comm.modularity(student_graph, communities))




# =================================================================================

# Create adjacency matrix
bi_adj = nx.adjacency_matrix(bipartite_graph)
student_adj = nx.adjacency_matrix(student_graph)
class_adj = nx.adjacency_matrix(class_graph)


# Adjacency matrix operations
bi_path = bi_adj * bi_adj * bi_adj
student_path = student_adj * student_adj * student_adj
class_path = class_adj * class_adj * class_adj


# Find loops
bi_loop_matrix = bi_path * bi_adj
student_loop_matrix = student_path * student_adj
class_loop_matrix = class_path * class_adj

bi_loop = find_diag(bi_loop_matrix)
student_loop = find_diag(student_loop_matrix)
class_loop = find_diag(class_loop_matrix)


# Create Graph Laplacian
bi_lap = nx.laplacian_matrix(bipartite_graph)
student_lap = nx.laplacian_matrix(student_graph)
class_lap = nx.laplacian_matrix(class_graph)


# Calculate Eigenvalues of the Graph Laplacian
bi_eigen = nx.laplacian_spectrum(bipartite_graph)
student_eigen = nx.laplacian_spectrum(student_graph)
class_eigen = nx.laplacian_spectrum(class_graph)



# # Cut set stuff
# bi_avg_node_cut, bi_avg_edge_cut = find_cut_sets(bipartite_graph)
# student_avg_node_cut, student_avg_edge_cut = find_cut_sets(student_graph)
# class_avg_node_cut, class_avg_edge_cut = find_cut_sets(class_graph)
#
# bi_min_node_cut = len(nx.algorithms.connectivity.cuts.minimum_node_cut(bipartite_graph))
# bi_min_edge_cut = len(nx.algorithms.connectivity.cuts.minimum_edge_cut(bipartite_graph))
# student_min_node_cut = len(nx.algorithms.connectivity.cuts.minimum_node_cut(student_graph))
# student_min_edge_cut = len(nx.algorithms.connectivity.cuts.minimum_edge_cut(student_graph))
# class_min_node_cut = len(nx.algorithms.connectivity.cuts.minimum_node_cut(class_graph))
# class_min_edge_cut = len(nx.algorithms.connectivity.cuts.minimum_edge_cut(class_graph))
#
# student_split = [['Reading', 'Projansky', 'Knollmeyer', 'Ross', 'Young', 'Golden', 'Miller', 'Wheeler', 'Dodes', 'Mosbarger', 'Napier Smith'],
#                  ['Molnar', 'Sisk', 'Bedward', 'Feldman', 'Banks', 'Komissar', 'Adair', 'Nolan', 'Nguyen', 'Sognamillo', 'Wintermute']]
#
# student_split_cut = nx.algorithms.cuts.cut_size(student_graph, student_split[0], student_split[1])
#
#
# with open("Class Network Script Output.txt", 'w') as file_object:
#     print("Bipartite graph:\nAverage node cut set size: " + str(bi_avg_node_cut) + "\nAverage edge cut set size: " + str(bi_avg_node_cut), file=file_object)
#     print("Minimum node cut set size: " + str(bi_min_node_cut) + "\nMinimum edge cut set size: " + str(bi_min_node_cut), file=file_object)
#     print("Student graph:\nAverage node cut set size: " + str(student_avg_node_cut) + "\nAverage edge cut set size: " + str(student_avg_edge_cut), file=file_object)
#     print("Minimum node cut set size: " + str(student_min_node_cut) + "\nMinimum edge cut set size: " + str(student_min_node_cut), file=file_object)
#     print("Class graph:\nAverage node cut set size: " + str(class_avg_node_cut) + "\nAverage edge cut set size: " + str(class_avg_edge_cut), file=file_object)
#     print("Minimum node cut set size: " + str(class_min_node_cut) + "\nMinimum edge cut set size: " + str(class_min_node_cut), file=file_object)
#     print("The minimum edge cut set for the graph partitioned by MATH 510 course year: " + str(student_split_cut), file=file_object)
#

# Create images of adjacency matrices with plt.spy
# plt.spy(student_lap, markersize=1)
# plt.savefig("testfile")


# Create matrix figures with matshow
# plt.matshow(student_lap.toarray())
# plt.savefig("testfile.png")


# Create heatmaps of Laplacians and path matrices
# matrix = sns.heatmap(class_path.toarray())
# fig = matrix.get_figure()
# fig.savefig("Class Paths.svg")


# Store values in 'Class Network Script Output.txt'
# with open("Class Network Script Output.txt", 'w') as file_object:
#     print("Graph Laplacian Spectra:", file=file_object)
#     print("Bipartite Eigenvalues:", file=file_object)
#     print_array(bi_eigen, file_obj=file_object, numpy="True")
#     print("Student Eigenvalues:", file=file_object)
#     print_array(student_eigen, file_obj=file_object, numpy="True")
#     print("Class Eigenvalues:", file=file_object)
#     print_array(class_eigen, file_obj=file_object, numpy="True")
#
#     print("Loops of length four:", file=file_object)
#     print("Bipartite loops of length four:", file=file_object)
#     print_array(bi_loop, file_obj=file_object, dense=True)
#     print("Student loops of length four:", file=file_object)
#     print_array(student_loop, file_obj=file_object, dense=True)
#     print("Class loops of length four:", file=file_object)
#     print_array(class_loop, file_obj=file_object, dense=True)
#
#     print("Adjacency matrices:", file=file_object)
#     print("Bipartite Adjacency Matrix:", file=file_object)
#     print_array(bi_adj, file_obj=file_object)
#     print("Student Adjacency Matrix:", file=file_object)
#     print_array(student_adj, file_obj=file_object)
#     print("Class Adjacency Matrix:", file=file_object)
#     print_array(class_adj, file_obj=file_object)
#
#     print("Paths of length three:", file=file_object)
#     print("Bipartite paths of length three:", file=file_object)
#     print_array(bi_path, file_obj=file_object)
#     print("Student paths of length three:", file=file_object)
#     print_array(student_path, file_obj=file_object)
#     print("Class paths of length three:", file=file_object)
#     print_array(class_path, file_obj=file_object)
#
#     print("Graph Laplacians:", file=file_object)
#     print("Bipartite Graph Laplacian:", file=file_object)
#     print_array(bi_lap, file_obj=file_object)
#     print("Student Graph Laplacian:", file=file_object)
#     print_array(student_lap, file_obj=file_object)
#     print("Class Graph Laplacian:", file=file_object)
#     print_array(class_lap, file_obj=file_object)
