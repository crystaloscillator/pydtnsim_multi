#!/bin/sh -x
for p in 50 90
do
    for n in 10 20 50 100 200
    do
        for i in `seq 10`
        do
            pydtnsim -M Log -n $n -s $i | p-coverage -n $n -p $p
        done >log-q1-$n-$p
    done
done

for n in 10 20 50 100 200
do
    stats -v log-q1-$n-50 | pick-mean-and-conf95 > log-q1-$n-50-cut
done
