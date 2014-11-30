.SUFFIXES = .cpp .o
CC        = g++
CFLAGS    = -g -ggdb -Wall -std=c++11 -I"." -O2
LDFLAGS   = -g -ggdb -Wall
CPPFLAGS  = ${CFLAGS}
objects   =	specie.o reaction.o parameter.o relation.o population.o totalPopulation.o randomGenerator.o output.o model.o nativeListLoader.o

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
