#!/bin/bash
set -e
                    
# python bespoke-multiplex-ranked-choice/label_nodes.py ./data/dkpol_edgelist_layer{i}.txt 3 5 ./data/dkpol_labels.txt
# python bespoke-multiplex-ranked-choice/run_bespoke.py ./data/dkpol_edgelist_layer{i}.txt 3 ./data/dkpol_training.txt 50 \
#                                         ./data/dkpol_labels.txt ./data/dkpol_bespoke.txt --eval_src ./data/dkpol_communities.txt

# python bespoke-main/label_nodes.py ./data/dkpol_edgelist_layer0.txt 5 ./data/dkpol_labels.txt
# python bespoke-main/run_bespoke.py ./data/dkpol_edgelist_layer0.txt ./data/dkpol_training.txt 50 \
#                                         ./data/dkpol_labels.txt ./data/dkpol_bespoke.txt --eval_src ./data/dkpol_communities.txt

outfile="./results.txt"
tmpfile='./res.tmp'

N=1000
L=3
C=50
Pin=0.95
Pout=0.05
Nfeats=4
Cfind=$(($N / 5))

echo "N $N L $L C $C Pin $Pin Pout $Pout Nfeats $Nfeats" > $outfile

python make_multiplex.py -N $N -m $L -c $C -pin $Pin -pout $Pout -name MyGraph

echo "Ranked Choice" >> $outfile
python bespoke-multiplex-ranked-choice/label_nodes.py MyGraph_edgelist_layer{i}.txt $L $Nfeats MyGraph_labels.txt > $tmpfile
python bespoke-multiplex-ranked-choice/run_bespoke.py MyGraph_edgelist_layer{i}.txt $L MyGraph_training.txt $Cfind \
                                        MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt > $tmpfile
tail -1 $tmpfile
tail -1 $tmpfile >> $outfile
echo "Weighted" >> $outfile
python bespoke-multiplex-weighted/combine_graph.py MyGraph_edgelist_layer{i}.txt --layers $L\
                                          --out MyGraph_edgelist_layer_combined.txt
python bespoke-multiplex-weighted/label_nodes.py MyGraph_edgelist_layer_combined.txt $Nfeats MyGraph_labels.txt > $tmpfile
python bespoke-multiplex-weighted/run_bespoke.py MyGraph_edgelist_layer_combined.txt MyGraph_training.txt $Cfind \
                                                 MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt  > $tmpfile
tail -1 $tmpfile
tail -1 $tmpfile >> $outfile
echo "Layer-wise" >> $outfile
for ((i=0 ; i<$L ; i++));
do
    python bespoke-main/label_nodes.py "MyGraph_edgelist_layer${i}.txt" $Nfeats MyGraph_labels.txt > $tmpfile
    python bespoke-main/run_bespoke.py "MyGraph_edgelist_layer${i}.txt" MyGraph_training.txt $Cfind \
        MyGraph_labels.txt MyGraph_bespoke.txt --eval_src MyGraph_communities.txt  >> $tmpfile
    tail -1 $tmpfile
    tail -1 $tmpfile >> $outfile
done
