set -e

# python make_multipartite.py -N 1000 -r 2 -c 25 -pin 0.8 -pout 0.2 -name MyGraph
# python bespoke-multipartite/label_nodes.py MyGraph_edgelist.txt 5 MyGraph_labels.txt
# python bespoke-multipartite/run_bespoke.py MyGraph_edgelist.txt MyGraph_training.txt 25 \
#                                            MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt

#python make_multiplex.py -N 1000 -m 2 -c 25 -pin 0.9 -pout 0.1 -name MyGraph
python make_multiplex.py -N 3000 -m 3 -c 50 -pin 0.95 -pout 0.01 -name MyGraph
#python bespoke-multiplex/label_nodes.py MyGraph_edgelist_layer0.txt 5 MyGraph_labels.txt
#python bespoke-multiplex/run_bespoke.py MyGraph_edgelist_layer0.txt MyGraph_training.txt 25 \
#                                        MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt
#python bespoke-multiplex/label_nodes.py MyGraph_edgelist_layer1.txt 5 MyGraph_labels.txt
#python bespoke-multiplex/run_bespoke.py MyGraph_edgelist_layer1.txt MyGraph_training.txt 25 \
#                                        MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt

python bespoke-multiplex-weighted/combine_graph.py MyGraph_edgelist_layer0.txt MyGraph_edgelist_layer1.txt MyGraph_edgelist_layer2.txt\
                                          --out MyGraph_edgelist_layer_combined.txt


python bespoke-multiplex-weighted/label_nodes.py MyGraph_edgelist_layer_combined.txt 3 MyGraph_labels.txt
python bespoke-multiplex-weighted/run_bespoke.py MyGraph_edgelist_layer_combined.txt MyGraph_training.txt 500 \
                                                 MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt
