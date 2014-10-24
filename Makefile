.SUFFIXES = .cpp .o
CC        = g++
CFLAGS    = -g -ggdb -Wall -std=c++11 -I"."
LDFLAGS   = -g -ggdb -Wall
CPPFLAGS  = ${CFLAGS}
objects   =	specie.o reaction.o parameter.o relation.o population.o totalPopulation.o randomGenerator.o output.o

.cpp.o:
	${CC} -o $@ -c ${CPPFLAGS} $<

pdmmod: ${objects} main.o
	${CC} ${LDFLAGS} -o $@ $^

test%: tests/test%.o ${objects}
	${CC} ${LDFLAGS} -o $@ $^

lisaTestst: lisaTestst.o

clean:
	${RM} ${objects} tests/*.o main.o specie

all: pdmmod
