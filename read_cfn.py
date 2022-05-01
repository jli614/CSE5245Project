import pickle
from make_multiplex import MulitplexCommunityNetwork
from collections import defaultdict

class MultiplexCFN:
    def __init__(self, f):
        self.f = f
        self.nmap = {}
        counter = 0
        self.communities = defaultdict(set)
        with open(f'{f}.gt') as fp:
            for line in fp:
                line=line.strip().split(',')
                if line[0] not in self.nmap:
                    self.nmap[line[0]] = counter
                    counter += 1
                self.communities[line[1]].add(self.nmap[line[0]])
        self.edges = defaultdict(set)
        with open(f'{f}.mpx') as fp:
            for line in fp:
                line = line.strip().split(',')
                self.edges[line[-1]].add((self.nmap[line[0]], self.nmap[line[1]]))
        self.c = len(self.communities)

    def write_graph(self):
        for i, clab in enumerate(self.edges):
            with open(f'{self.f}_edgelist_layer{i}.txt', 'w') as fp:
                for edge in self.edges[clab]:
                    fp.write(f'{edge[0]}\t{edge[1]}\n')
                for node in self.nmap.values():
                    fp.write(f'{node}\t{node}\n')
        
        t='\t'
        with open(f'{self.f}_communities.txt', 'w') as fp:
            for community in self.communities.values():
                fp.write(f'{t.join(map(str, sorted(community)))}\n')

        with open(f'{self.f}_training.txt', 'w') as fp:
            for i, community in enumerate(self.communities.values()):
                if i > self.c // 2:
                    break
                fp.write(f'{t.join(map(str, sorted(community)))}\n')
    

def main():
    # load the data
    f1 = './data/aucs'
    f2 = './data/dkpol'
    files = [f2]

    for f in files:
        mpx = MultiplexCFN(f)
        mpx.write_graph()

if __name__ == '__main__':
    main()
