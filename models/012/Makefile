# List of objects specific to this model - append your objects here!
modelObjects    = model.o nativeListLoader.o main.o

# Path to the libpdmmod directory
libPdmmodDir    = ../../libpdmmod
CFLAGS          = -std=c++11 -g -ggdb -Wall -I"." -I"${libPdmmodDir}" -O2

# Loading list of library objects and prepending the libpdmmod directory to each entry
include ${libPdmmodDir}/Makefile.lib
libraryObjects = $(foreach object, ${localLibraryObjects}, ${libPdmmodDir}/${object})

.SUFFIXES       = .cpp .o
CC              = g++
LDFLAGS         = -g -ggdb -Wall
CPPFLAGS        = ${CFLAGS}

.cpp.o:
	${CC} -o $@ -c ${CPPFLAGS} $<

pdmmod: ${libraryObjects} ${modelObjects}
	${CC} ${LDFLAGS} -o $@ $^

clean:
	${RM} ${libraryObjects} ${modelObjects} pdmmod

all: pdmmod
