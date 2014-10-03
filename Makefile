.SUFFIXES = .cpp .o
CC        = g++
CFLAGS    = -D_HAS_EXCEPTIONS=0 -I../../src -I../../Demos/OpenGL -O2 -msse2 -ffast-math -m64 -fno-rtti -fno-exceptions
LDFLAGS   = -lGL -lGLU -lglut -L../../lib -s -m64 -L/usr/lib64
#CFLAGS    = -g -ggdb -Wall
#LDFLAGS   = -g -ggdb -Wall
CPPFLAGS  = ${CFLAGS}
objects   =	Box2dDemo.o main.o ANNQueue.o misc.o \
						ANNDirect.o
#						ANNHiddenRecursive.o
include Makefile.libs
libs      = ${libOpenGLSupport} ${libBulletDynamics} \
            ${libBulletCollision} ${libLinearMath}

tadrosim-graphics: CFLAGS += -DWITH_GRAPHICS

.cpp.o:
	${CC} -o $@ -c ${CPPFLAGS} $<

tadrosim: ${objects}
	${CC} ${LDFLAGS} -o $@ $^ ${libs}

tadrosim-graphics: clean tadrosim
	mv tadrosim tadrosim-graphics
	${RM} ${objects}

clean:
	${RM} ${objects} tadrosim

all: tadrosim
