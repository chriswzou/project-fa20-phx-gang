#!/bin/sh
for f in inputs/small/*.in ;
    do
    g=${f%.in} ;
    python solver_bf_better.py $f out/$g.out ;
    done