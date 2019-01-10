#!/bin/sh -x
for n in 10 20 50 100
do
    for i in `seq 10`
    do
        pydtnsim -M Log -n $n -s $i | p-coverage -n $n -p 50
    done >log-$n
    echo -n "$n "
    stats -v log-$n | pick-mean-and-conf95
done

