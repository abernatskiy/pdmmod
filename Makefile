.SUFFIXES = .cpp .o
CC        = g++
CFLAGS    = -g -ggdb -Wall -std=c++11
LDFLAGS   = -g -ggdb -Wall
CPPFLAGS  = ${CFLAGS}
objects   =	specie.o reaction.o parameter.o population.o totalPopulation.o

.cpp.o:
	${CC} -o $@ -c ${CPPFLAGS} $<

specie: ${objects} main.o
	${CC} ${LDFLAGS} -o $@ $^

testParam: testParam.o parameter.o
	${CC} ${LDFLAGS} -o $@ $^

testSpecie: testSpecie.o ${objects}
	${CC} ${LDFLAGS} -o $@ $^

testPopulation: testPopulation.o ${objects}
	${CC} ${LDFLAGS} -o $@ $^

testTotalPopulation: testTotalPopulation.o ${objects}
	${CC} ${LDFLAGS} -o $@ $^

lisaTestst: lisaTestst.o

clean:
	${RM} ${objects} test*.o specie main.o

all: specie
