import pandas as pd
import numpy as np
import csv
import json
import scipy.sparse as sp
import networkx as nx
# import re
# import itertools
# from collections import Counter
# from scipy.spatial import distance
import matplotlib.pyplot as plt
import matplotlib.font_manager as fmgr
# import statistics as stat
# from array import array

######################### Cooccurence Matrix ########################

# function: JSON to list
def json2List(file):
    with open (file, encoding="utf-8-sig") as f:
        data = json.load(f)
    return data

# function: CSV to list
def csv2List(file):
    with open (file, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

# function: flatten list
def flatten(list):
    flat_list = [item for sublist in list for item in sublist]
    return(flat_list)

# function: generate-occurence matrix
def getCoocMat(target_words, translated, document):
    voc2id1 = dict(zip(target_words, range(len(target_words))))
    voc2id2 = dict(zip(translated, range(len(translated))))
    rows, cols, vals = [], [], []
    for r, d in enumerate(document):
        for e in d:
            # print("e is ", e)
            if voc2id1.get(e) is not None:
                # print("r is ", r)
                rows.append(r)
                cols.append(voc2id1[e])
                vals.append(1)
    X = sp.csr_matrix((vals, (rows, cols))) # sparse matrix for faster calculation
    Xc = X.T.dot(X) # coocurrence matrix
    cooc = pd.DataFrame(
        Xc.todense(), # turn sparse matrix to dense matrix
        index = translated,
        columns = translated
    )
    # jaccard_matrix = 1 - distance.cdist(Xc.todense(), Xc.todense(), 'jaccard')
    #cooc_jaccard = pd.DataFrame(jaccard_matrix, index=target_words, columns=target_words)
    return cooc

# function: get nodes
def getNodes(target_words, target_words_cnt, cooc):
    nodes = []
    for i in range(len(target_words)):
        for j in range(i+1, len(target_words)):
            connection = cooc.iat[i, j]
            if connection > 0:
                nodes.append([
                    target_words[i], 
                    target_words[j], 
                    target_words_cnt[i], 
                    target_words_cnt[j], 
                    connection
                ])
    return nodes

# function: get nodes for certain words
# function: get words nodes
def getCertainNodes(target, target_words, target_words_cnt, cooc):
    nodes = []
    i = target_words.index(target)
    connection_list = cooc[target]
    connection_list = connection_list[1:100]
    for j in range(1, len(connection_list)):
        connection = connection_list[j]
        nodes.append([
            target, 
            target_words[j], 
            target_words_cnt[i], 
            target_words_cnt[j], 
            connection
        ])
    return nodes

# load data
pro_china_bow = json2List("../data/taiwan/taiwan_cut/pro_china_bow.json")
pro_china_nouns = csv2List("../data/taiwan/nouns/top1000/pro_china_nouns_1000.csv")[1:900]
pro_china_count = [item[1] for item in pro_china_nouns]
pro_china_ch = [item[0] for item in pro_china_nouns]
pro_china_ko = [item[2] + f"({item[0]})" for item in pro_china_nouns]
pro_china_en = [item[3] + f"({item[0]})" for item in pro_china_nouns]

tw_libertytimes_bow = json2List("../data/taiwan/taiwan_cut/tw_libertytimes_bow.json")
tw_libertytimes_nouns = csv2List("../data/taiwan/nouns/top1000/tw_libertytimes_nouns_1000.csv")[1:900]
tw_libertytimes_count = [item[1] for item in tw_libertytimes_nouns]
tw_libertytimes_ch = [item[0] for item in tw_libertytimes_nouns]
tw_libertytimes_ko = [item[2] + f"({item[0]})" for item in tw_libertytimes_nouns]
tw_libertytimes_en = [item[3] + f"({item[0]})" for item in tw_libertytimes_nouns]

tw_nextapple_bow = json2List("../data/taiwan/taiwan_cut/tw_nextapple_bow.json")
tw_nextapple_nouns = csv2List("../data/taiwan/nouns/top1000/tw_nextapple_nouns_1000.csv")[1:900]
tw_nextapple_count = [item[1] for item in tw_nextapple_nouns]
tw_nextapple_ch = [item[0] for item in tw_nextapple_nouns]
tw_nextapple_ko = [item[2] + f"({item[0]})" for item in tw_nextapple_nouns]
tw_nextapple_en = [item[3] + f"({item[0]})" for item in tw_nextapple_nouns]

# generate coocurence matrix
cooc_nextapple = getCoocMat(tw_nextapple_ch, tw_nextapple_ko, flatten(tw_nextapple_bow))
cooc_libertytimes = getCoocMat(tw_nextapple_ch, tw_libertytimes_ko, flatten(tw_libertytimes_bow))
cooc_pro_china = getCoocMat(pro_china_ch, pro_china_ko, flatten(pro_china_bow))

# get nodes list
# nodes_nextapple = getNodes(tw_nextapple_ko, tw_nextapple_count, cooc_nextapple)
nodes_nextapple = getCertainNodes("항중보대(抗中保台)", tw_nextapple_ko, tw_nextapple_count, cooc_nextapple)
nodes_libertytimes = getCertainNodes("항중보대(抗中保台)", tw_libertytimes_ko, tw_libertytimes_count, cooc_libertytimes)
nodes_pro_china = getCertainNodes("항중보대(抗中保台)", pro_china_ko, pro_china_count, cooc_pro_china)

###############################################################
######################## Draw graph ###########################
###############################################################

# function: draw network graph
def netGraph(node_data, cut_level):
    G = nx.Graph()

    cut = np.percentile([pair[4] for pair in node_data], cut_level)
    min_connect = np.min([pair[4] for pair in node_data])
    max_connect = np.max([pair[4] for pair in node_data])
    
    for pair in node_data:
        node_x, node_y, node_x_cnt, node_y_cnt, connection = pair[0], pair[1], pair[2], pair[3], pair[4]
        if not G.has_node(node_x):
            G.add_node(node_x, count=node_x_cnt)
        if not G.has_node(node_y):
            G.add_node(node_y, count=node_y_cnt)
        if not G.has_edge(node_x, node_y):
            if connection > cut:
                G.add_edge(
                    node_x, node_y, 
                    weight=connection/100, 
                    color = "red", 
                    alpha = (connection - min_connect) / (max_connect - min_connect)
                )
            else:
                G.add_edge(
                    node_x, node_y, 
                    weight=connection/100, 
                    color = "lightgrey", 
                    alpha = (connection - min_connect) / (max_connect - min_connect)
                )
    
            
    # G.nodes(data=True) # check data
    # G.edges(data=True) # check data
    pos = nx.spring_layout(G, k=1.2) # assign positions of nodes
    
    # node_size = [int(d['count'])/10 for (n,d) in G.nodes(data=True)]
    # pagerank_score_dict = nx.pagerank(G)
    # pagerank_score = [item for item in pagerank_score_dict.values()]
    # pagerank_median = stat.median(pagerank_score)
    # pagerank_score = [((item * 1000)**5) * 100 for item in pagerank_score_dict.values()]
    # pagerank_score = [item*100000 for item in pagerank_score_dict.values()]
    # edge_width = [float(d['weight'])*20 for (u,v,d) in G.edges(data=True)]

    edge_width = [float(d['weight'])/2 for (u,v,d) in G.edges(data=True)]
    edge_color = [d['color'] for (u,v,d) in G.edges(data=True)]
    edge_alpha = [d['alpha'] for (u,v,d) in G.edges(data=True)]

    # font_prop = fmgr.FontProperties(fname="/System/Library/Fonts/PingFang.ttc")
    
    plt.clf()
    plt.figure(figsize=(15,15))

    ### draw nodes
    # nx.draw_networkx_nodes(G, pos, node_size=pagerank_score, node_color="grey", alpha=0.5)
    # draw labels
    # for node, (x, y) in pos.items():
    #     if pagerank_score_dict[node] >= pagerank_median:
    #         plt.text(x, y, node, fontsize=((pagerank_score_dict[node] * 500)**5 * 5), 
    #                  ha='center', va='center', font_properties=font_prop)

    # nx.draw_networkx_labels(G, pos, font_family= "PingFang HK")
    fmgr.fontManager.addfont("/Users/chanhyuk/projects/china_taiwan/NotoSansCJK-SC/NotoSansCJKsc-Regular.ttf")
    nx.draw_networkx_labels(G, pos, font_family= "Noto Sans CJK SC")
    # [f.name for f in fmgr.fontManager.ttflist if re.match(r"Noto Sans.+", f.name)]
    
    ### draw edges
    # for (u, v, d) in G.edges(data=True):
    #     if d['weight'] > 0.1:
    #         nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color='green', width=edge_width, alpha=1)
    #     else:
    #         nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color='green', width=edge_width, alpha=1)
    
    nx.draw_networkx_edges(G, pos, edge_color="black", width=1, alpha=edge_alpha)
    
    
    # [nx.draw_networkx_edges(G, pos, edgelist=[(u,v)], edge_color='black', width=edge_width, alpha=[d['weight']/1000]) for (u, v, d) in G.edges(data=True)]
    
    plt.axis('off')
    # plt.show()

# generate network graphs
netGraph(nodes_nextapple, 100)
plt.savefig('../figures/nextapple_항중보대.png')

netGraph(nodes_libertytimes, 100)
plt.savefig('../figures/libertytimes_항중보대.png')

netGraph(nodes_pro_china, 100)
plt.savefig('../figures/pro_china_항중보대.png')
