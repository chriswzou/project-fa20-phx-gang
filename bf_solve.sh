#!/bin/sh
for f in inputs/medium/*.in ;
    do
    g=${f%.in} ;
    python solver_bf_better.py $f out/$g.out ;
    done
