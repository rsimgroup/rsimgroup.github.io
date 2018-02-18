HEADERS = ac3dparse   glwin      light     pngfile    sphere     ui\
apitrigeom  grid       machine   ppm        tachyon    util\
box         hash       macros    quadric    texture    vector\
camera      image      mgfparse  render     tgafile    vol\
coordsys    imageio    nffparse  ring       threads    winbmp\
cylinder    imap       parallel  rtcommon   trace\
extvol      intersect  parse     sgirgb     trackball\
getargs     jpeg       parvol    shade      triangle\
global      jsinterp   plane     spaceball  types


SRC =  tgafile ac3dparse  getargs    jpeg       pngfile    sphere     util \
api        global     light      ppm        texture    vector \
apigeom    glwin      main       quadric    vol \
box        grid       mgfparse   render     threads    winbmp \
camera     hash       nffparse   ring       trace \
coordsys   imageio    parallel   sgirgb     trackball \
cylinder   imap       parse      shade      triangle \
extvol     intersect  plane      spaceball  ui 

TARGET = tachyon

USERLIBS = -lm -lpthread
USERFLAGS = -DTHR -DNUM_THREADS=1 -DUSEPOSIXTHREADS

USE_PENTIUM_M =  -vec- -march=pentium4 -mcpu=pentium4
LIBDIR = /usr/lib

LD = /opt/intel_cc_80/bin/icc

STATLINK = -dn # Option to force static linkage
CC = /opt/intel_cc_80/bin/icc

OPTIMIZE = $(USE_GPROF) $(USE_PENTIUM_M) -g -O3 #-Wall

CFLAGS = $(OPTIMIZE) $(USERFLAGS) $(USE_DISP) $(USE_SHMEM) $(INCLUDEDIR) $(TRACE) \
$(VERBOSE) $(VERIFY) $(WARNINGS)

OBJS = $(SRC:%=obj/%.o)

execs/$(TARGET).out: $(OBJS)
	$(LD) $(STATLINK) $(CFLAGS) $(LIBRARYDIR) -o execs/$(TARGET) $(OBJS) $(LIBS) $(USERLIBS)

$(OBJS): $(HEADERS:%=src/%.h) $(SRC:%=src/%.c)
	$(CC) -o $@ $(CFLAGS) -c $(*:obj/%=src/%.c)

clean:
	rm -f obj/*.o execs/$(TARGET)

