HEADERS =  config global mpeg2enc vlc
SRC =  conform fdctref puthdr readpic stats putmpg idct putpic transfrm \
putseq motion mpeg2enc putvlc writepic predict quantize \
putbits ratectl

TARGET = mpeg2enc

# Use the first one if no threading is needed
# The second USERLIBS is for thread support

#USERLIBS = -lm
USERLIBS = -lm -lpthread

# INT_IDCT is for Integer IDCT, gives better performance. Use -DINT_IDCT to 
# enable. QUIET suppresses all standard outputs, use -DQUIET to enable. For 
# thread support, use the 2nd USERFLAGS and enter the desired number of threads.

USE_THREADS = -DLTHREAD -DNUM_THREADS=1
#USE_INT_DCT = -DINT_DCT
#USE_SSE2 = -use_msasm -DSSE2

USERFLAGS = $(USE_SSE2) $(USE_THREADS) $(USE_INT_DCT) -DQUIET


LIBDIR = /usr/lib

LD = gcc #/opt/intel_cc_80/bin/icc       # Using GCC as the compiler for now
STATLINK = -dn # Option to force static linkage
CC = gcc #/opt/intel_cc_80/bin/icc
OPTIMIZE = -g -O3 -Wall

LIBS = $(USERLIBS)
CFLAGS = $(OPTIMIZE) $(USERFLAGS)
OBJS = $(SRC:%=obj/%.o)

execs/$(TARGET).out: $(OBJS)
	$(LD) $(STATLINK) $(USERFLAGS) -o execs/$(TARGET) $(OBJS) $(LIBS)

$(OBJS): $(HEADERS:%=src/%.h) $(SRC:%=src/%.c)
	$(CC) -o $@ $(CFLAGS) -c $(*:obj/%=src/%.c)

clean:
	rm -f obj/*.o execs/$(TARGET)


