import networkx as nx
import pickle as pkl
from operator import itemgetter



def creat_graph(node_file,name_dict_file, percent = 0.2):
    
    with open("single_node.pkl","rb") as f:
        single_node = pkl.load(f)

    with open(name_dict_file,"rb") as f:
        name_dict = pkl.load(f)

    with open(node_file,"rb") as f:
        nodes_list = pkl.load(f)   


    nodes_list.sort( key = itemgetter(2), reverse = True)
    nodes_list = nodes_list[:int(len(nodes_list) * percent)]
    

    nodes = []    

    for item in nodes_list:
        first_node = name_dict[item[0] - 1]
        second_node = name_dict[item[1] - 1]
        edge = item[2]

        nodes.append((first_node,second_node,edge))

    


    G = nx.Graph()
    for node_key,node_value in single_node.items():
        G.add_node(node_key,weight = node_value)

    G.add_weighted_edges_from(nodes)
    nx.write_gml(G,"my_graph.gml")


    
if __name__ == '__main__':
    creat_graph("all_nodes.pkl","name_index_dict.pkl")