import sys, numpy, os, random, time
from . import common, train
from sklearn.cluster import KMeans
from collections import defaultdict

def get_seed(gt_size, seed_dict):
    degree_start = gt_size-1
    degree_end = degree_start
    eps = 5
    while True:
        if degree_end in seed_dict:
            ordered_list = seed_dict[degree_end].ordered_list
            if len(ordered_list) != 0:
                seed, score = ordered_list.pop(0)
                return seed, degree_end
        degree_end+=1
        if degree_end - degree_start>eps:
            return None, degree_end

def get_seed_ranked(gt_size, seeds_by_layer_group, group_id, n=10, exclude=[]):
    scores = defaultdict(int)
    degrees = defaultdict(list)
    for i in seeds_by_layer_group:
        tops = get_top_seeds(gt_size, seeds_by_layer_group[i][group_id], n=n)
        for i, (seed, new_deg) in enumerate(tops):
            scores[seed] += n - i
            degrees[seed].append(new_deg)
    while scores:
        seed = max(scores, key = lambda c: scores[c])
        if seed in exclude:
            scores.pop(seed)
        else:
            new_deg = random.sample(degrees[seed],1)
            return seed, new_deg
    return None, gt_size

def get_top_seeds(gt_size, seed_dict, n=10):
    #seed dict is degree -> list of seeds
    degree_start = gt_size-1
    nodes = []
    eps = 0
    while len(nodes) < n:
        if degree_start + eps in seed_dict:
            ordered_list = seed_dict[degree_start + eps].ordered_list
            if len(ordered_list) != 0:
                nodes.extend(ordered_list)
        if degree_start - eps in seed_dict:
            ordered_list = seed_dict[degree_start - eps].ordered_list
            if len(ordered_list) != 0:
                nodes.extend(ordered_list)
        eps+=1
    return nodes

def get_supports(size_dist_per_group):
    d = {}
    tot = float(sum(list(map(len, size_dist_per_group.values()))))
    for g_id in size_dist_per_group:
        supp = len(size_dist_per_group[g_id])
        d[g_id] = supp/tot
    return d

def pick_pattern(pattern_supports):
    r = random.random()
    s = 0
    for patt_id in pattern_supports:
        s+=pattern_supports[patt_id]
        if s > r:
            return patt_id
    return patt_id

def pick_size(size_dist):
    return random.sample(size_dist,1)[0]

def get_comms(nw, num_find, seeds_by_layer_group, size_dist_per_group, KM_obj, node_labels, unique_seeds, rep_th=2):
    found_size_pat_dist = {}
    comms_list = []
    seen = {}
    pattern_supports = get_supports(size_dist_per_group)
    while len(comms_list) < num_find:
        group_id = pick_pattern(pattern_supports)
        size_dist = size_dist_per_group[group_id]
        size = pick_size(size_dist)
        ### first key is layer, second key is group. This is an indexing problem!
        seed, new_deg = get_seed_ranked(size, seeds_by_layer_group, group_id)
        if unique_seeds:
            exclude = set()
            while seen.get(seed, 0) > rep_th:
                exclude.add(seed)
                seed, new_deg = get_seed_ranked(size, seeds_by_layer_group, exclude=exclude)
        ### Start growing (Stopped here)
        comm = nw.rand_subgraph_nodes(size, seed)
        if len(comm)>=common.MIN_COM_SIZE:
            comms_list.append(comm)
            if unique_seeds:
                for n in comm:
                    if n not in seen:
                        seen[n]=0
                    seen[n]+=1
    return comms_list

def main(nw_src, layers, gt_src, node_label_src, num_find, nclus, verbose=True, unique_seeds=False):
    start = time.time()
    gts = common.load_comms(gt_src, verbose=False)
    if len(gts) == 0:
        print("Error! No training communities of size >3 found. Cannot run Bespoke.")
        return None
    if len(gts) < nclus:
        print("Error! Too few (<#patterns,",nclus,") training communities of size >3 found. Cannot run Bespoke.")
        return None
    node_labels = common.load_labels(node_label_src)
    nw = common.load_MultiNW_graph(nw_src, layers)

    if len(nw.nodes()) != len(node_labels.keys()):
        print("Error! Number of labeled nodes does not match number of nodes in the graph. #NW nodes=", len(nw.nodes()),"#labeled nodes=", len(node_labels.keys()))
        return None
    if verbose:
        print("Training...")
        sys.stdout.flush()
    ret_list = train.train(nw, layers, gts, node_labels, nclus)

    if verbose:
        print("Training complete...\nBeginning extraction...")
        sys.stdout.flush()
    KM_obj, size_dist_per_group, seed_info_per_group_by_layer = ret_list
    end_train = time.time()
    comms = get_comms(nw, num_find, seed_info_per_group_by_layer, size_dist_per_group, KM_obj, node_labels, unique_seeds)
    end = time.time()
    tot_time, train_time = round(end-start,2),round(end_train-start,2)

    if verbose:
        print("Extraction complete.")
        sys.stdout.flush()
    return comms, KM_obj, tot_time, train_time
