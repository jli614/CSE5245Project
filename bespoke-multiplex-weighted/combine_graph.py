import numpy, sys, time, os
from modules import common
from sklearn.cluster import KMeans
from scipy.stats.mstats import zscore
from collections import Counter
import argparse

def run(graph_src, outfile, verbose=False):

    #print(graph_src[0])
    #g1 = common.load_SimpleNW_graph(graph_src[0])
    
    #for i in range(1, len(graph_src)):

    new_dict = {}

    for src in graph_src:
        #src = graph_src[i]
        print(src)
        g = common.load_SimpleNW_graph(src)

        new_dict = Counter(new_dict) + Counter(g.edge_weights_dict)

    print(len(new_dict))
    #print(g1)

    f = open(outfile, "w")
    for k, v in new_dict.items():
        #print(str(k[0]) + "\t" + str(k[1]) + "\t" + str(v) + "\n")
        f.write(str(k[0]) + "\t" + str(k[1]) + "\t" + str(v) + "\n")
        

def get_parser():
    parser = argparse.ArgumentParser(description='Description: Script to run node labeling on a given graph. \
                                     Please refer to the readme for details about each argument.')
    parser.add_argument('nw_src', help='Graph file. One edge per line.', nargs='*')
    parser.add_argument('--out', help='')
    parser.add_argument('--verbose', help='enable verbosity.', action="store_true")
    return parser

if __name__ == '__main__':
    parser = get_parser()
    try:
        a = parser.parse_args()
    except:
        exit()

    graph_src = a.nw_src
    outfile = a.out
    verbose = a.verbose

    run(graph_src, outfile, verbose)
