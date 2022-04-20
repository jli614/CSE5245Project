set -e

python make_multipartite.py -N 1000 -r 2 -c 25 -pin 0.8 -pout 0.2 -name MyGraph
python bespoke-multipartite/label_nodes.py MyGraph_edgelist.txt 5 MyGraph_labels.txt
python bespoke-multipartite/run_bespoke.py MyGraph_edgelist.txt MyGraph_training.txt 20 \
                                           MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt
