import networkx as nx
import numpy as np
from collections import defaultdict
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', type=int, default=1000)
    parser.add_argument('-m', type=int, default=2)
    parser.add_argument('-c', type=int, default=25)
    parser.add_argument('-pin', type=float, default=0.8)
    parser.add_argument('-pout', type=float, default=0.2)
    parser.add_argument('-name', type=str, default='MyGraph')
    return parser.parse_args()

class MulitplexCommunityNetwork:
    def __init__(self, N, m, c, p_in, p_out, name='MyGraph'):
        self.N = N
        self.m = m
        self.c = c
        self.name = name
        self.communities, self.community_map = self.map_nodes(self.c)
        self.edges = self.make_edges(p_in, p_out)

    def map_nodes(self, p):
        mapping = {}
        sets = defaultdict(set)
        for n in range(self.N):
            set_id = np.random.randint(p)
            mapping[n] = set_id
            sets[set_id].add(n)
        return sets, mapping

    def make_edges(self, p_in, p_out):
        edges = defaultdict(set())
        for i in range(self.m):
            for n1 in range(self.N):
                for n2 in range(n1):
                    rval = np.random.uniform()
                    if self.community_map[n1] == self.community_map[n2]:
                        pval = p_in
                    else:
                        pval = p_out

                    if rval < pval:
                        edges[i].add((n2, n1))
            return edges

    def make_graph(self):
        Gs = defaultdict(nx.Graph)
        for i in range(self.m):
            for n in range(N):
                Gs[i].add_node(n, partition=self.partition_map[n], community=self.community_map[n])
            Gs[i].add_edges_from(self.edges[i])
        return Gs

    def write_graph(self):
        for i in range(self.m):
            with open(f'{self.name}_edgelist_layer{i}.txt', 'w') as fp:
                for edge in self.edges[i]:
                    fp.write(f'{edge[0]}\t{edge[1]}\n')
        
        t='\t'
        with open(f'{self.name}_communities.txt', 'w') as fp:
            for community in self.communities.values():
                fp.write(f'{t.join(map(str, sorted(community)))}\n')

        with open(f'{self.name}_training.txt', 'w') as fp:
            for i, community in enumerate(self.communities.values()):
                if i > self.c // 5:
                    break
                fp.write(f'{t.join(map(str, sorted(community)))}\n')

def main():

    args = parse_args()

    MP = MulitplexCommunityNetwork(args.N, args.m, args.c, args.pin, args.pout, args.name)
    MP.write_graph()

if __name__ == '__main__':
    main()