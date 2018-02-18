#ifdef RSIM

#define VEC_STRIDE_SET  0
#define VEC_FLUSH       1
#define VEC_MGAU_EVAL_LOAD 2
#define VEC_MGAU_EVAL 4
#define VEC_FREE 9

#define SIMD_MGAU_EVAL 10

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
