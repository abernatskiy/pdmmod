#!/bin/bash
#$ -S /bin/bash
#$ -N run13
#$ -cwd
#$ -q cpu_long@node061
#$ -pe openmpi 1
#$ -P kenprj

cd /cavern/eliza/origins/pdmmod/stochKit/
python runtimes.py
