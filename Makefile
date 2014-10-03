.SUFFIXES = .cpp .o
CC        = g++
CFLAGS    = -g -ggdb -Wall
LDFLAGS   = -g -ggdb -Wall
CPPFLAGS  = ${CFLAGS}
objects   =	specie.o main.o


.cpp.o:
	${CC} -o $@ -c ${CPPFLAGS} $<

specie: ${objects}
	${CC} ${LDFLAGS} -o $@ $^ ${libs}


clean:
	${RM} ${objects} specie

all: specie
