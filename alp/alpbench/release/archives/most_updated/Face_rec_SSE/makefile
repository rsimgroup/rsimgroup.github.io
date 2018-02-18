HEADERS =  csuCommon csuCommonUtil csuCommonMatrix csuCommonFile \
csuCommonSubspace csuCommonCommandLine csuCommonImage threading

SRC =  csuCommonUtil csuCommonMatrix csuCommonFile csuCommonSubspace \
csuCommonCommandLine csuCommonImage csuSubspaceProject csuSubspaceEigen \
csuSubspaceFisher csuSubspaceCVEigen threading

TARGET = face_project_nosse

# Uncomment USE_THREADS if multithreading is desired. Use THREAD_NUM to specify
# number of threads.

THREAD_NUM =1 
USE_THREADS = -DTHRD -DNUM_THREADS=$(THREAD_NUM)
#USE_SSE2 = -use_msasm -DSSE2
USE_VTUNE = -DVTUNE


USERFLAGS = $(USE_VTUNE) $(USE_THREADS) $(USE_SSE2) 
USERLIBS = -lm #-lpthread 

LIBDIR = /usr/lib
USE_PENTIUM_M = -vec- -vec_report5 -march=pentium4 -mcpu=pentium4
#-march=pentiumiii -mcpu=pentiumpro
#USE_GPROF = -p

LD = /opt/intel_cc_80/bin/icc       # Using GCC as the compiler for now
#STATLINK = -dn # Option to force static linkage
CC = /opt/intel_cc_80/bin/icc
OPTIMIZE = -g -O3 #-Wall

VTUNE_INCL = -I/opt/intel/vtune/analyzer/include
VTUNE_LIB =-L/opt/intel/vtune/analyzer/bin -lVtuneApi 

LIBS = $(USERLIBS) $(VTUNE_LIB) 
CFLAGS =  $(USE_GPROF) $(USE_PENTIUM_M) $(OPTIMIZE) $(USERFLAGS) $(VTUNE_INCL)
OBJS = $(SRC:%=obj/%.o)

execs/$(TARGET).out: $(OBJS)
	$(LD) $(USE_GPROF) $(STATLINK) $(USERFLAGS) -o execs/$(TARGET) $(OBJS) $(LIBS)

$(OBJS): $(HEADERS:%=src/%.h) $(SRC:%=src/%.c)
	$(CC) -o $@ $(CFLAGS) -c $(*:obj/%=src/%.c)

clean:
	rm -f obj/*.o execs/$(TARGET)

