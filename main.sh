set -e

# python make_multipartite.py -N 2000 -r 2 -c 25 -pin 0.9 -pout 0.05 -name MyGraph
# python bespoke-multipartite/label_nodes.py MyGraph_edgelist.txt 5 MyGraph_labels.txt
# python bespoke-multipartite/run_bespoke.py MyGraph_edgelist.txt MyGraph_training.txt 25 \
#                                            MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt

python make_multiplex.py -N 3000 -m 3 -c 50 -pin 0.95 -pout 0.01 -name MyGraph

python bespoke-multiplex-ranked-choice/label_nodes.py MyGraph_edgelist_layer{i}.txt 3 5 MyGraph_labels.txt
python bespoke-multiplex-ranked-choice/run_bespoke.py MyGraph_edgelist_layer{i}.txt 3 MyGraph_training.txt 500 \
                                        MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt

python bespoke-main/label_nodes.py MyGraph_edgelist_layer0.txt 5 MyGraph_labels.txt
python bespoke-main/run_bespoke.py MyGraph_edgelist_layer0.txt MyGraph_training.txt 500 \
                                        MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt
