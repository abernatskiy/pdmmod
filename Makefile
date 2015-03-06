.SUFFIXES       = .cpp .o
CC              = g++
CFLAGS          = -g -ggdb -Wall -std=c++11 -I"." -O2
LDFLAGS         = -g -ggdb -Wall
CPPFLAGS        = ${CFLAGS}
engineObjects   = reaction.o relation.o population.o randomGenerator.o totalPopulation.o
modelObjects    = models/current/model.o
ioObjects       = output.o nativeListLoader.o inih/cpp/INIReader.o inih/ini.o parametersLoader.o parameter.o
objects         = ${engineObjects} ${modelObjects} ${ioObjects}

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
