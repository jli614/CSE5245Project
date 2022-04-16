import networkx as nx
import numpy as np
from collections import defaultdict

class MulitpartiteCommunityNetwork:
    def __init__(self, N, r, c, p_in, p_out, name='MyGraph'):
        self.N = N
        self.r = r
        self.c = c
        self.name = name
        self.partitions, self.partition_map = self.map_nodes(self.r)
        self.communities, self.community_map = self.map_nodes(self.c)
        self.edges = self.make_edges(p_in, p_out)

    def map_nodes(self, p_in, p_out):
        mapping = {}
        sets = defaultdict(set)
        for n in range(self.N):
            set_id = np.random.randint(p)
            mapping[n] = set_id
            sets[set_id].add(n)
        return sets, mapping

    def make_edges(self, p_in, p_out):
        edges = set()
        for n1 in range(N):
            for n2 in range(n1):
                if self.partition_map[n1] == self.partition_map[n2]:
                    continue
            
                rval = np.random.uniform()
                if self.community_map[n1] == self.community_map[n2]:
                    pval = p_in
                else:
                    pval = p_out

                if rval < pval:
                    edges.add((n2, n1))
        return edges

    def make_graph(self):
        G = nx.Graph()
        for n in range(N):
            G.add_node(n, partition=self.partition_map[n], community=self.community_map[n])
        G.add_edges_from(self.edges)
        return G

    def write_graph(self):
        with open(f'{name}_edgelist.txt', 'w') as fp:
            for edge in self.edges:
                fp.write(f'{edge[0]} {edge[1]}\n')
        
        with open(f'{name}_communities.txt', 'w') as fp:
            for community in self.communities:
                fp.write(f'{" ".join(map(str, sorted(community)))}\n')
        
        with open(f'{name}_partitions.txt', 'w') as fp:
            for partition in self.partitions:
                fp.write(f'{" ".join(map(str, sorted(partition)))}\n')
