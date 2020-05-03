#!/bin/bash

for month in 2020/* ; do
	ls $month/*.tex | awk '{printf "\input{%s}\n", $1}' > 2020/${month##*/}.tex
done
