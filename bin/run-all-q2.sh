#!/bin/sh -x
n=100
for p in 50 90
do
    for r in 10 50 100 200
    do
        for i in `seq 10`
        do
            pydtnsim -M Log -n $n -s $i -r $r | p-coverage -n $n -p $p
        done >log-q2-$n-$p-$r
    done
done

for r in 10 50 100 200
do
    stats -v log-q2-$n-50-$r | pick-mean-and-conf95 > log-q2-$n-50-$r-cut
done
