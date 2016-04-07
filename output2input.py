
inputFile = '/tmp/output.txt'
outputFile = '/tmp/populations.txt'

fi = open(inputFile,'r')
line = fi.read().split(',')[1:-1]
fo = open(outputFile,'a')
for item in line:
    fo.write(item+'\n')
fo.close()
fi.close()

