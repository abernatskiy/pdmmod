.SUFFIXES = .cpp .o
CC        = g++
CFLAGS    = -g -ggdb -Wall -std=c++11
LDFLAGS   = -g -ggdb -Wall
CPPFLAGS  = ${CFLAGS}
objects   =	specie.o main.o reaction.o parameter.o

.cpp.o:
	${CC} -o $@ -c ${CPPFLAGS} $<

specie: ${objects}
	${CC} ${LDFLAGS} -o $@ $^ ${libs}

testParam: testParam.o parameter.o
	${CC} ${LDFLAGS} -o $@ testParam.o parameter.o

testSpecie: testSpecie.o specie.o reaction.o parameter.o

testPopulation: testPopulation.o population.o specie.o parameter.o

clean:
	${RM} ${objects} specie

all: specie
