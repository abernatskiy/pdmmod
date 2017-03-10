#!/bin/bash

numTraj=10000

# Generate the random seeds library
# Take sha1, truncate to four least signifcant hex digits, convert to decimal, store in file with labels
for i in `seq -w 0 ${numTraj}`; do
  #echo "ibase=16; `echo $i | sha1sum | cut -d ' ' -f 1 | cut -c 37- | tr /a-z/ /A-Z/`" | bc | sed -e "s/^/${i} /";
	SEED=`od -vAn -N4 -tu4 < /dev/urandom`
	echo $SEED
done > seeds
