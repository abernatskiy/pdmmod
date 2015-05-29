#!/bin/bash
#$ -S /bin/bash
#$ -N stochkit
#$ -cwd
#$ -q cpu_long@node061
#$ -pe openmpi 1
#$ -P kenprj

cd /cavern/eliza/origins/pdmmod/stochKit/
/home/eliza/anaconda3/bin/python runtimes.py
