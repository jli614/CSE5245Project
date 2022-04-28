import copy, random
from collections import defaultdict

class MultiNW:
    def __init__(self):
        self.neighbors_dict = {}
        self.edge_set = {}
        self.node_set = set()
        self.edge_weights = {}

    def load_ugraph_from_file(self, mx_src, layers, delim, verbose=False):
        '''
        load undirected graph from text file
        of form node1 <delim> node2 per line
        to dict, d[node1]=set(adj nodes)
        '''
        for i in range(layers):
            src = mx_src.replace('{i}', str(i))
            self.neighbors_dict[i] = {}
            self.edge_set[i] = set()
            self.edge_weights[i] = {}
            num_edges = 0
            f = open(src,'r')
            for line in f:
                num_edges+=1
            f.close()
            f = open(src, 'r')
            counter = 0
            for line in f:
                line = line.strip()
                if line == "" or line[0] == "#":
                    continue
                else:
                    parts = line.split(delim)
                    a,b = list(map(int,parts[:2]))
                    if a == b:
                        continue
                    if a not in self.neighbors_dict[i]:
                        self.neighbors_dict[i][a] = set()
                    if b not in self.neighbors_dict[i]:
                        self.neighbors_dict[i][b] = set()
                    self.neighbors_dict[i][a].add(b)
                    self.neighbors_dict[i][b].add(a)
                    edge = tuple(sorted([a,b]))
                    self.edge_set[i].add(edge)
                    self.node_set.add(a)
                    self.node_set.add(b)
                    if len(parts) == 3:
                        weight = float(parts[2])
                        self.edge_weights[i][edge] = weight
                    if verbose:
                        if counter%10000 == 0:
                            print(100*float(counter)/num_edges,"% done")
                    counter+=1
            f.close()

    def neighbors(self, node, i):
        return copy.deepcopy(self.neighbors_dict[i][node])

    def degree(self, node, i):
        return len(self.neighbors_dict[i][node])

    def set_nodeset(self, nodeset):
        self.node_set = nodeset

    def set_edgeset(self, edgeset, i):
        self.edge_set[i] = edgeset

    def set_edgeweights(self, weights, i):
        self.edge_weights[i] = weights

    def set_neighbors(self, neighbors_d, i):
        self.neighbors_dict[i] = neighbors_d

    def add_edge(self, edge, i, weight=None):
        nodeA, nodeB = edge
        self.node_set.add(nodeA)
        self.node_set.add(nodeB)
        edge = tuple(sorted(edge))
        self.edge_set[i].add(edge)
        self.neighbors_dict[i].setdefault(nodeA,set()).add(nodeB)
        self.neighbors_dict[i].setdefault(nodeB, set()).add(nodeA)
        if weight!=None:
            self.edge_weights[i][edge] = weight

    def get_copy(self):
        x = copy.deepcopy(self)
        return x

    def nodes(self):
        return copy.copy(self.node_set)

    def edges(self, i):
        return copy.copy(self.edge_set[i])

    def rand_subgraph_nodes(self, size, seed=None):
        if seed is None:
            seed = random.sample(self.node_set, 1)[0]
        nodes = set()
        nodes.add(seed)
        seeds = set(nodes)
        old_size = len(nodes)
        while len(nodes)<size:
            node_sets = defaultdict(set)
            for i in self.neighbors_dict:
                node_sets[i] = self.grow(seeds, size, nodes, i)
            seeds = set.intersection(*node_sets.values())
            nodes.update(seeds)

            if len(nodes) == old_size:
                break
            old_size = len(nodes)
        return nodes

    def grow(self, seeds, target, cur_nodes, i):
        grown_nodes = set()
        for node in seeds:
            neigh = self.neighbors_dict[i][node]
            for n in neigh:
                if (len(cur_nodes) + len(grown_nodes)) < target:
                    if n not in cur_nodes:
                        grown_nodes.add(n)
                else:
                    break
            if (len(cur_nodes) + len(grown_nodes)) > target:
                break
        return grown_nodes

    def get_rand_subgraphs(self, dist, num_graphs, i, prob=1, use_diff_seeds=False, decay_rate=1):
        rand_subsets = []
        nodes = set(self.nodes())
        if dist == None:
            dist = []
            for i in range(num_graphs):
                val = random.randint(4,100)
                dist.append(val)

        while len(rand_subsets) < num_graphs:
            seed = None
            for size in dist:
                r = self.rand_subgraph_nodes(size, seed)
                rand_subsets.append(r)

                if use_diff_seeds:
                    nodes.difference_update(set(r))
                    seed = None
                    if len(nodes)>0:
                        seed = random.sample(nodes, 1)[0]

                if len(rand_subsets)>num_graphs:
                    break
        return rand_subsets

    def subgraph(self, node_set, i):
        '''
        return SimpleNW object containing graph
        induced on this object using nodes in
        node_list.
        '''
        subgraph = self.__class__()
        subgraph.set_nodeset(node_set)
        edge_set = set()
        edge_weights = {}
        sub_neigh = {}
        for node in node_set:
            sub_neigh.setdefault(node,set())
            neigh = self.neighbors_dict[i][node]
            for n in neigh:
                if n in node_set:
                    edge = tuple(sorted([n,node]))
                    edge_set.add(edge)
                    sub_neigh[node].add(n)
                    if edge in self.edge_weights[i]:
                        edge_weights[edge] = self.edge_weights[i][edge]
        subgraph.set_edgeset(edge_set, i)
        subgraph.set_neighbors(sub_neigh, i)
        subgraph.set_edgeweights(edge_weights, i)
        return subgraph

    def get_weight(self, edge, i):
        edge = tuple(sorted(edge))
        if edge in self.edge_weights[i]:
            return self.edge_weights[i][edge]
        else:
            return None

    def get_connected_components(self, i):
        ccs = []
        target = len(self.node_set)
        remaining = copy.copy(self.node_set)
        while len(remaining)>0:
            seed = remaining.pop()
            reach = self.rand_subgraph_nodes(target, seed, i)
            ccs.append(reach)
            remaining.difference_update(reach)
        return ccs
