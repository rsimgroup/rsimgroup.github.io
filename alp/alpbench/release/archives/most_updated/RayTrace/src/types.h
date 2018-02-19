/* 
 * types.h - This file contains all of the type definitions for the raytracer
 *
 *  $Id: types.h,v 1.95 2004/02/03 06:05:32 johns Exp $
 */

#ifndef TYPES_H
#define TYPES_H 1

#include "rtcommon.h" /* defintions common to all interfaces */

struct ray_t;

#ifdef USESINGLEFLT
/* All floating point types will be based on "float" */
#define SPEPSILON   0.0001f     /* amount to crawl down a ray           */
#define EPSILON     0.0001f     /* amount to crawl down a ray           */
#define FHUGE       1e18f       /* biggest fp number we care about      */
#define TWOPI       6.28318531f /* guess... :-)                         */
#define MINCONTRIB  0.001959f   /* 1.0 / 512.0, smallest contribution   */
                                /* to overall pixel color we care about */
#else
/* All floating point types will be based on "double" */
#define SPEPSILON   0.000001    /* amount to crawl down a ray           */
#define EPSILON     0.000001    /* amount to crawl down a ray           */
#define FHUGE       1e18        /* biggest fp number we care about      */
#define TWOPI       6.28318531  /* guess... :-)                         */
#define MINCONTRIB  0.001959    /* 1.0 / 512.0, smallest contribution   */
                                /* to overall pixel color we care about */
#endif

#define BOUNDTHRESH 16         /* subdivide cells /w > # of children   */

/* 
 * Maximum internal table sizes 
 * Use prime numbers for best memory system performance
 * (helps avoid cache aliasing..)
 */
#define MAXIMGS   39         /* maxiumum number of distinct images   */

/* 
 * Ray flags 
 *
 * These are used in order to skip calculations which are only
 * needed some of the time.  For example, when shooting shadow
 * rays, we only have to find *one* intersection that's valid, 
 * if we find even one, we can quit early, thus saving lots of work.
 */
#define RT_RAY_REGULAR   1  /* A regular ray, fewer shorcuts available    */
#define RT_RAY_SHADOW    2  /* A shadow ray, we can early-exit asap       */
#define RT_RAY_FINISHED  4  /* We've found what we're looking for already */
                            /* early-exit at soonest opportunity..        */

/* 
 * Texture flags
 * 
 * These are used in order to skip calculations that are only needed
 * some of the time.
 */
#define RT_TEXTURE_NOFLAGS    0 /* No options set             */
#define RT_TEXTURE_SHADOWCAST 1 /* This object casts a shadow */ 
#define RT_TEXTURE_ISLIGHT    2 /* This object is a light     */


typedef unsigned char byte; /* 1 byte */

typedef struct {
   flt x;        /* X coordinate value */
   flt y;        /* Y coordinate value */
   flt z;        /* Z coordinate value */
} vector;


typedef struct {
   float r;      /* Red component   */
   float g;      /* Green component */
   float b;      /* Blue component  */
} color;


typedef struct {
   byte r;       /* Red component   */
   byte g;       /* Green component */
   byte b;       /* Blue component  */
} bytecolor;


typedef struct {         /* Raw 24 bit image structure, for tga, ppm etc */
  int loaded;            /* image memory residence flag    */
  int xres;              /* image X axis size              */
  int yres;              /* image Y axis size              */
  int bpp;               /* image bits per pixel           */
  char name[96];         /* image filename (with path)     */
  unsigned char * data;  /* pointer to raw byte image data */
} rawimage;


typedef struct {
  int levels;
  rawimage const ** images;
} mipmap;


typedef struct {         /* Scalar Volume Data */
  int loaded;            /* Volume data memory residence flag */
  int xres;		 /* volume X axis size                */
  int yres;		 /* volume Y axis size                */
  int zres;		 /* volume Z axis size                */
  flt opacity;		 /* opacity per unit length           */
  char name[96];         /* Volume data filename              */
  unsigned char * data;  /* pointer to raw byte volume data   */
} scalarvol;


#define RT_TEXTURE_HEAD \
  color (* texfunc)(const void *, const void *, void *);                 \
  unsigned int flags; /* texturing/lighting flags */                     \
  flt ambient;        /* ambient lighting */                             \
  flt diffuse; 	      /* diffuse reflection */                           \
  flt phong;          /* phong specular highlights */                    \
  flt phongexp;       /* phong exponent/shininess factor */              \
  int phongtype;      /* phong type: 0 == plastic, nonzero == metal */   \
  flt specular;       /* specular reflection */                          \
  flt opacity;        /* how opaque the object is */ 


typedef struct {
  RT_TEXTURE_HEAD
} texture;

typedef struct {
  RT_TEXTURE_HEAD
  color  col;         /* base object color */
  vector ctr;         /* origin of texture */
  vector rot;         /* rotation of texture about origin */
  vector scale;       /* scale of texture in x,y,z */
  vector uaxs;	      /* planar map U axis */
  vector vaxs;	      /* planar map V axis */
  void * img;         /* pointer to image for image mapping */
  void * obj;         /* object ptr, hack for vol shaders */
} standard_texture;

typedef struct {
  RT_TEXTURE_HEAD
  void * obj;         /* object ptr, hack for vcstri for now */
  color c0;           /* color for vertex 0 */
  color c1;           /* color for vertex 1 */
  color c2;           /* color for vertex 2 */
} vcstri_texture;


typedef struct {
  void (* intersect)(const void *, void *);        /* intersection func ptr  */
  void (* normal)(const void *, const void *, const void *, void *); /* normal function ptr    */
  int (* bbox)(void *, vector *, vector *);        /* return the object bbox */
  void (* freeobj)(void *);                        /* free the object        */
} object_methods;
 

#define RT_OBJECT_HEAD \
  unsigned int id;           /* Unique Object serial number    */ \
  void * nextobj;            /* pointer to next object in list */ \
  object_methods * methods;  /* this object's methods          */ \
  texture * tex;             /* object texture                 */ 
	

typedef struct {
  RT_OBJECT_HEAD
} object; 


typedef struct {
  const object * obj;        /* to object we hit                        */ 
  flt t;                     /* distance along the ray to the hit point */
} intersection;


typedef struct {
  int num;                   /* number of intersections    */
  intersection closest;      /* closest intersection > 0.0 */
} intersectstruct;



typedef struct {
  int projection;            /* camera projection mode                  */
  vector center;             /* center of the camera in world coords    */
  vector viewvec;            /* view direction of the camera  (Z axis)  */
  vector rightvec;           /* right axis for the camera     (X axis)  */
  vector upvec;              /* up axis for the camera        (Y axis)  */
  flt camzoom;               /* zoom factor for the camera              */
  flt px;                    /* width of image plane in world coords    */
  flt py;                    /* height of image plane in world coords   */
  flt psx;                   /* width of pixel in world coords          */
  flt psy;                   /* height of pixel in world coords         */
  flt focallength;           /* distance from eye to focal plane        */
  flt left;                  /* left side of perspective frustum        */
  flt right;                 /* right side of perspective frustum       */
  flt top;                   /* top side of perspective frustum         */
  flt bottom;                /* bottom side of perspective frustum      */
  flt aperture;              /* depth of field aperture                 */
  vector projcent;           /* center of image plane in world coords   */
  color (* cam_ray)(void *, flt, flt);   /* camera ray generator fctn   */
  vector lowleft;            /* lower left corner of image plane        */
  vector iplaneright;        /* image plane right vector                */
  vector iplaneup;           /* image plane up    vector                */
} camdef;

typedef struct fogdata_t {
  color (* fog_fctn)(struct fogdata_t *, color, flt);  /* fogging function */
  color col;                 /* fog color                               */
  flt start;                 /* fog start parameter                     */
  flt end;                   /* fog end parameter                       */
  flt density;               /* fog density parameter                   */
} fogdata;

typedef struct {
  int numcpus;               /* number of processors on this node       */
  flt cpuspeed;              /* relative speed of cpus on this node     */
  flt nodespeed;             /* relative speed index for this node      */
  char machname[512];        /* machine/node name                       */
} nodeinfo;

typedef struct list {
  void * item;
  struct list * next;
} list;

typedef struct {
  vector hit;  /* ray object intersection hit point */
  vector N;    /* surface normal at the hit point */
  vector L;    /* vector point in the direction from hit point to the light */
  flt    Llen; /* distance from hit point to the light (if any) */
} shadedata;

typedef struct {
  object * boundedobj;       /* bounded object list, starts out empty   */
  object * unboundedobj;     /* unbounded object list, starts out empty */
  int numobjects;            /* number of objects in group              */
} displist;
 
typedef struct {
  char outfilename[200];     /* name of the output image                */
  int writeimagefile;        /* enable/disable writing of image to disk */
  unsigned char * img;       /* pointer to a raw rgb image to be stored */
  int imginternal;           /* image was allocated by the library      */
  int imgformat;             /* output format for final image           */
  int numthreads;            /* user controlled number of threads       */
  int nodes;                 /* number of distributed memory nodes      */
  int mynode;                /* my distributed memory node number       */
  nodeinfo * cpuinfo;        /* overall cpu/node/threads info           */
  int hres;                  /* horizontal output image resolution      */
  int vres;                  /* vertical output image resolution        */
  flt aspectratio;           /* aspect ratio of output image            */
  int raydepth;              /* maximum recursion depth                 */
  int antialiasing;          /* number of antialiasing rays to fire     */
  int verbosemode;           /* verbose reporting flag                  */
  int boundmode;             /* automatic spatial subdivision flag      */
  int boundthresh;           /* threshold number of subobjects          */
  list * texlist;            /* linked list of texture objects          */
  camdef camera;             /* camera definition                       */
  color (* shader)(void *);  /* main shader used for the whole scene    */  
  flt (* phongfunc)(const struct ray_t * incident, const shadedata * shadevars, flt specpower);              /* phong shader used for whole scene       */ 
  int transmode;             /* transparency mode                       */
  color background;          /* scene background color                  */
  fogdata fog;               /* fog parameters                          */
  displist objgroup;         /* objects in the scene                    */
  list * lightlist;          /* linked list of lights in the scene      */
  int numlights;             /* number of lights in the scene           */
  int scenecheck;            /* re-check scene for changes              */
  void * parbuf;             /* parallel message passing handle         */
  void * threads;            /* thread handles                          */
  void * threadparms;        /* thread parameters                       */
} scenedef;


typedef struct ray_t {
   vector o;             /* origin of the ray X,Y,Z                        */
   vector d;             /* normalized direction of the ray                */
   flt maxdist;          /* maximum distance to search for intersections   */
   flt opticdist;        /* total distance traveled from camera so far     */  
   void (* add_intersection)(flt, const object *, struct ray_t *); 
   intersectstruct intstruct; /* ptr to thread's intersection data         */ 
   unsigned int depth;   /* levels left to recurse.. (maxdepth - curdepth) */
   unsigned int flags;   /* ray flags, any special treatment needed etc    */
   unsigned long serial; /* serial number of the ray                       */
   unsigned long * mbox; /* mailbox array for optimizing intersections     */
   scenedef * scene;     /* pointer to the scene, for global parms such as */
                         /* background colors etc                          */
   unsigned int randval; /* random number seed                             */
} ray;


/* a proposed structure to pass to shader helper functions */
/* this might help organize the shading code in a much nicer way */
typedef struct {  
  ray * incident; 
  object * obj;  
  texture * tex;
  vector pnt;
  vector N;
} shadeinfo;  


#endif
