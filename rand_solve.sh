#!/bin/sh
for f in inputs/large/*.in ;
    do
    g=${f%.in} ;
    python solver-random-1.py $f out/$g.out ;
    done
