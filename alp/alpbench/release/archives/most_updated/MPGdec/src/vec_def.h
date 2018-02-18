#ifdef RSIM

#define VEC_STRIDE_SET   0
#define VEC_CLEAR_BLK    1
#define VEC_SATURATE     2
#define VEC_IDCT         5

#define VEC_FLUSH           14

#define VEC_FORM_COMP_PRED  15
#define VEC_FORM_COMP_PRED2 30
#define VEC_FORM_COMP_PRED3 45

#define SIMD_SATURATE          60
#define SIMD_IDCT              64
#define SIMD_FORM_COMP_PRED    70

#define SIMD_ADD_BLK  80
#define VEC_ADD_BLK   90
#define SIMD_CLEAR_BLK 85

#define BEGIN_VEC1Arg(x)           BeginVec1Arg(x);
#define BEGIN_VEC2Arg(x,y)         BeginVec2Arg(x,y);
#define BEGIN_VEC3Arg(x,y,z)       BeginVec3Arg(x,y,z);
#define BEGIN_VEC4Arg(x,y,z,p)     BeginVec4Arg(x,y,z,p);
#define BEGIN_VEC5Arg(x,y,z,p,q)   BeginVec5Arg(x,y,z,p,q);
#define BEGIN_VEC6Arg(x,y,z,p,q,r) BeginVec5Arg(x,y,z,p,q,r);
#define END_VECNoRet()             EndVecNoRet();
#define END_VEC()                  EndVec();

#else /* NotRSIM */

#define BEGIN_VEC1Arg(x)           0
#define BEGIN_VEC2Arg(x,y)         0
#define BEGIN_VEC3Arg(x,y,z)       0
#define BEGIN_VEC4Arg(x,y,z,p)     0
#define BEGIN_VEC5Arg(x,y,z,p,q)   0
#define BEGIN_VEC6Arg(x,y,z,p,q,r) 0
#define END_VECNoRet()             (0)
#define END_VEC()                  (0)

#endif
