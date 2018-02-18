/* idct.c, inverse fast discrete cosine transform                           */

/* Copyright (C) 1996, MPEG Software Simulation Group. All Rights Reserved. */

/*
 * Disclaimer of Warranty
 *
 * These software programs are available to the user without any license fee or
 * royalty on an "as is" basis.  The MPEG Software Simulation Group disclaims
 * any and all warranties, whether express, implied, or statuary, including any
 * implied warranties or merchantability or of fitness for a particular
 * purpose.  In no event shall the copyright-holder be liable for any
 * incidental, punitive, or consequential damages of any kind whatsoever
 * arising from the use of these programs.
 *
 * This disclaimer of warranty extends to the user of these programs and user's
 * customers, employees, agents, transferees, successors, and assigns.
 *
 * The MPEG Software Simulation Group does not represent or warrant that the
 * programs furnished hereunder are free of infringement of any third-party
 * patents.
 *
 * Commercial implementations of MPEG-1 and MPEG-2 video, including shareware,
 * are subject to royalty fees to patent holders.  Many of these patents are
 * general enough such that they are unavoidable regardless of implementation
 * design.
 *
 */

/**********************************************************/
/* inverse two dimensional DCT, Chen-Wang algorithm       */
/* (cf. IEEE ASSP-32, pp. 803-816, Aug. 1984)             */
/* 32-bit integer arithmetic (8 bit coefficients)         */
/* 11 mults, 29 adds per DCT                              */
/*                                      sE, 18.8.91       */
/**********************************************************/
/* coefficients extended to 12 bit for IEEE1180-1990      */
/* compliance                           sE,  2.1.94       */
/**********************************************************/

/* this code assumes >> to be a two's-complement arithmetic */
/* right shift: (-2)>>1 == -1 , (-3)>>1 == -2               */

#include <math.h>
#include "config.h"
#include <assert.h>

#define W1 2841 /* 2048*sqrt(2)*cos(1*pi/16) */
#define W2 2676 /* 2048*sqrt(2)*cos(2*pi/16) */
#define W3 2408 /* 2048*sqrt(2)*cos(3*pi/16) */
#define W5 1609 /* 2048*sqrt(2)*cos(5*pi/16) */
#define W6 1108 /* 2048*sqrt(2)*cos(6*pi/16) */
#define W7 565  /* 2048*sqrt(2)*cos(7*pi/16) */
#define PI 3.14159265358979323846

/* global declarations */
void Initialize_Fast_IDCT _ANSI_ARGS_((void));
void Fast_IDCT _ANSI_ARGS_((short *block));

/* private data */
#if 0
static short iclip[1024]; /* clipping table */
#endif
static short *iclp;

__declspec(align(16)) short ic[8][8];

/* private prototypes */
static void idctrow _ANSI_ARGS_((short *blk));
static void idctcol _ANSI_ARGS_((short *blk));

/* row (horizontal) IDCT
 *
 *           7                       pi         1
 * dst[k] = sum c[l] * src[l] * cos( -- * ( k + - ) * l )
 *          l=0                      8          2
 *
 * where: c[0]    = 128
 *        c[1..7] = 128*sqrt(2)
 */

static void idctrow(blk)
short *blk;
{
  int x0, x1, x2, x3, x4, x5, x6, x7, x8;

  /* shortcut */
  if (!((x1 = blk[4]<<11) | (x2 = blk[6]) | (x3 = blk[2]) |
        (x4 = blk[1]) | (x5 = blk[7]) | (x6 = blk[5]) | (x7 = blk[3])))
  {
    blk[0]=blk[1]=blk[2]=blk[3]=blk[4]=blk[5]=blk[6]=blk[7]=blk[0]<<3;
    return;
  }

  x0 = (blk[0]<<11) + 128; /* for proper rounding in the fourth stage */

  /* first stage */
  x8 = W7*(x4+x5);
  x4 = x8 + (W1-W7)*x4;
  x5 = x8 - (W1+W7)*x5;
  x8 = W3*(x6+x7);
  x6 = x8 - (W3-W5)*x6;
  x7 = x8 - (W3+W5)*x7;
  
  /* second stage */
  x8 = x0 + x1;
  x0 -= x1;
  x1 = W6*(x3+x2);
  x2 = x1 - (W2+W6)*x2;
  x3 = x1 + (W2-W6)*x3;
  x1 = x4 + x6;
  x4 -= x6;
  x6 = x5 + x7;
  x5 -= x7;
  
  /* third stage */
  x7 = x8 + x3;
  x8 -= x3;
  x3 = x0 + x2;
  x0 -= x2;
  x2 = (181*(x4+x5)+128)>>8;
  x4 = (181*(x4-x5)+128)>>8;
  
  /* fourth stage */
  blk[0] = (x7+x1)>>8;
  blk[1] = (x3+x2)>>8;
  blk[2] = (x0+x4)>>8;
  blk[3] = (x8+x6)>>8;
  blk[4] = (x8-x6)>>8;
  blk[5] = (x0-x4)>>8;
  blk[6] = (x3-x2)>>8;
  blk[7] = (x7-x1)>>8;
}

/* column (vertical) IDCT
 *
 *             7                         pi         1
 * dst[8*k] = sum c[l] * src[8*l] * cos( -- * ( k + - ) * l )
 *            l=0                        8          2
 *
 * where: c[0]    = 1/1024
 *        c[1..7] = (1/1024)*sqrt(2)
 */
static void idctcol(blk)
short *blk;
{
  int x0, x1, x2, x3, x4, x5, x6, x7, x8;

  /* shortcut */
  if (!((x1 = (blk[8*4]<<8)) | (x2 = blk[8*6]) | (x3 = blk[8*2]) |
        (x4 = blk[8*1]) | (x5 = blk[8*7]) | (x6 = blk[8*5]) | (x7 = blk[8*3])))
  {
    blk[8*0]=blk[8*1]=blk[8*2]=blk[8*3]=blk[8*4]=blk[8*5]=blk[8*6]=blk[8*7]=
      iclp[(blk[8*0]+32)>>6];
    return;
  }

  x0 = (blk[8*0]<<8) + 8192;

  /* first stage */
  x8 = W7*(x4+x5) + 4;
  x4 = (x8+(W1-W7)*x4)>>3;
  x5 = (x8-(W1+W7)*x5)>>3;
  x8 = W3*(x6+x7) + 4;
  x6 = (x8-(W3-W5)*x6)>>3;
  x7 = (x8-(W3+W5)*x7)>>3;
  
  /* second stage */
  x8 = x0 + x1;
  x0 -= x1;
  x1 = W6*(x3+x2) + 4;
  x2 = (x1-(W2+W6)*x2)>>3;
  x3 = (x1+(W2-W6)*x3)>>3;
  x1 = x4 + x6;
  x4 -= x6;
  x6 = x5 + x7;
  x5 -= x7;
  
  /* third stage */
  x7 = x8 + x3;
  x8 -= x3;
  x3 = x0 + x2;
  x0 -= x2;
  x2 = (181*(x4+x5)+128)>>8;
  x4 = (181*(x4-x5)+128)>>8;
  
  /* fourth stage */
  blk[8*0] = iclp[(x7+x1)>>14];
  blk[8*1] = iclp[(x3+x2)>>14];
  blk[8*2] = iclp[(x0+x4)>>14];
  blk[8*3] = iclp[(x8+x6)>>14];
  blk[8*4] = iclp[(x8-x6)>>14];
  blk[8*5] = iclp[(x0-x4)>>14];
  blk[8*6] = iclp[(x3-x2)>>14];
  blk[8*7] = iclp[(x7-x1)>>14];
}

/* two dimensional inverse discrete cosine transform */
void Fast_IDCT(block)
short *block;
{
  if (0) {
    int i;
    for (i=0; i<8; i++)
      idctrow(block+8*i);
    
    for (i=0; i<8; i++)
      idctcol(block+i);
  } else {

    int i, j, k;
    int s;
    __declspec(align(16)) short tmp[64];
#ifdef SSE2
    short *b_p, *icp, *tmp_p, *b2_p;

    /* not the most elegant approach, can be improved with other fast IDCT 
       methods out there */
    
    b_p = block;/*block+8*i;*/
    icp = &ic[0][0];
    tmp_p = &tmp[0]; /*&tmp[8*i];*/
    b2_p = &block[63];

    /*	
    for (i=0; i<8; i++) {

      for (j=0; j<8; j++) {
      
        s=0;

        for (k=0; k<8; k++)
          s += ic[j][k] * block[8*i+k];          

        tmp[8*i+j] = s >> 15;
      }
    }
    */
    __asm 
	{
	  mov   ecx, [b2_p]          ;
	  mov   ebx, [b_p]        ; /*load blk ptr*/
	  mov   edx, [icp]       ; /*load ic ptr */
	  mov   eax, [tmp_p]    ;
      
	idct_row_loop:
	  movdqa   xmm0, [ebx]      ; /*load 8 shorts from block*/
	  movdqa   xmm1, [edx]         ; /*ic[0][0..7]*/
	  movdqa   xmm2, [edx+16]      ; /*ic[1][0..7]*/
	  movdqa   xmm3, [edx+32]      ; /*ic[2][0..7]*/
	  movdqa   xmm4, [edx+48]      ; /*ic[3][0..7]*/

	  movdqa   xmm7, [edx+64]      ; /*ic[4][0..7]*/

	  pmaddwd xmm1, xmm0     ; /* xmms : 4 32-bit partial sums */
	  pmaddwd xmm2, xmm0     ;
	  pmaddwd xmm3, xmm0     ;
	  pmaddwd xmm4, xmm0     ;
	  pmaddwd xmm7, xmm0     ;

	  movdqa  xmm5, xmm1     ;
	  movdqa  xmm6, xmm3     ;

	  unpcklpd xmm1, xmm2    ; /*xmm1: 2.1 2.0 1.1 1.0 */
	  unpckhpd xmm5, xmm2    ; /*xmm5: 2.3 2.2 1.3 1.2 */

	  movdqa   xmm2, [edx+80]      ; /*ic[5][0..7]*/

	  unpcklpd xmm3, xmm4    ;
	  unpckhpd xmm6, xmm4    ;

	  movdqa   xmm4, [edx+96]      ; /*ic[6][0..7]*/
	  pmaddwd  xmm2, xmm0    ;

	  paddd  xmm6, xmm3      ; 

	  movdqa   xmm3, [edx+112]      ; /*ic[7][0..7]*/
	  pmaddwd xmm4, xmm0     ;
	  pmaddwd xmm3, xmm0     ; /*2nd batch, 7,2,4,3 */

	  paddd  xmm5, xmm1      ; /*xmm5: 2.a 2.b | 1.a 1.b */

	  movdqa xmm1, xmm5      ;
	  shufps  xmm1, xmm6, 0x8d ; /* 1: 3.a, 2.a, 1.a, 0.a */
	  shufps  xmm5, xmm6, 0xd8 ; /* 5: 3.b, 2.b, 1.b, 0.b */
	  
	  movdqa xmm6, xmm7      ;

	  paddd  xmm1, xmm5      ;

	  movdqa xmm5, xmm4      ;
	  
	  unpcklpd xmm7, xmm2    ; /*xmm7: 2.1 2.0 1.1 1.0 */
	  unpckhpd xmm6, xmm2    ; /*xmm6: 2.3 2.2 1.3 1.2 */

	  unpcklpd xmm4, xmm3    ;
	  unpckhpd xmm5, xmm3    ;

	  paddd xmm6, xmm7       ;
	  paddd xmm5, xmm4       ;

	  movdqa xmm2, xmm6      ;
	  shufps  xmm2, xmm5, 0x8d ; /* 1: 3.a, 2.a, 1.a, 0.a */
	  shufps  xmm6, xmm5, 0xd8 ; /* 5: 3.b, 2.b, 1.b, 0.b */

	  paddd xmm2, xmm6       ;

	  psrad  xmm1, 15        ;
	  psrad  xmm2, 15         ;

	  packssdw xmm1, xmm2    ;

	  movdqa [eax], xmm1     ;

	  add   ebx, 16         ;
	  add   eax, 16         ;

	  cmp   ebx, ecx        ;
	  jb    idct_row_loop   ;
	  
	  ; /* start of second phase */
	mov edx, [tmp_p]        ; /* load tmp blk ptr */
	mov eax, [icp]          ; /* load coeffs table ptr*/
	mov ebx, [b_p]          ;
	mov edi, [b2_p]         ;

      idct_col_outer:
	movdqa xmm6, [eax]      ; /* load ic[0][0..7] */
	
	pxor xmm4, xmm4         ;
	pxor xmm5, xmm5         ;
	mov  ecx, 8             ;

      idct_col_loop:
	movdqa xmm1, [edx]      ; /* load tmp[0][0..7] */
	pshuflw xmm0, xmm6, 0   ; /* copy the lowest word to all positions */
	;pshuflw xmm0, xmm0, 0   ;
	pshufd xmm0, xmm0, 0
	psrldq  xmm6, 2         ; /* prepare for next word*/
	
	movdqa xmm2, xmm0       ;
	pmulhw xmm2, xmm1       ; /*multiply them */
	pmullw xmm0, xmm1       ; /*2 :high words 1: low words */

	movdqa xmm3, xmm0       ; /*3 : low words */
	punpckhwd xmm0,xmm2     ; /*1 : left half, 4 32-bit */
	punpcklwd xmm3,xmm2    ; /*3 : right half, 4 32-bit */

	paddd xmm4, xmm0      ; /*accumulate */
	paddd xmm5, xmm3      ; /*4 : left, 5 : right*/

	add  edx, 16          ;
	
	loop idct_col_loop    ; /* end of inner loop */

	sub  edx, 128           ;
	psrad xmm4, 15        ; /*s >> 15 */
	psrad xmm5, 15        ;
	
	packssdw xmm5, xmm4   ;

	movdqa [ebx], xmm5    ; /*store to block[i][j]*/

	add  ebx, 16          ;
	add  eax, 16          ;
	cmp  ebx, edi         ;
	jb   idct_col_outer   ;
      }

#else /* NON-SSE2 code */

    for (i=0; i<8; i++) { 

      for (j=0; j<8; j++) { 

	s = 0;
	
	for (k=0; k<8; k++)
	  s += ic[j][k] * block[8*i+k];          /* this is block[i][k] */
	tmp[8*i+j] = s >> 15;                         /* this is block[i][j] */

      }  /* for j */

    } /* for i */
    

    /* 	simd multiplication of AxB = C is done as follows:
	If col_dim(A) == N
  	To produce row C[0]

	For i=0 to N-1 {

		// each element in the 0th row of A is multiplied by
		// all elements in row B[i] and a running sum is kep in sum

		sum[0..N-1] = A[0][i] * B[k][0..N-1]   

	} 

	C[0][0..N]  = sum[0..N];

        If we do the above loop for all rows of A, we can produce C entirely.
   */



    for (j=0; j<8; j++) {
      

      for (i=0; i<8; i++) {

	s = 0;
	
	for (k=0; k<8; k++)
	  s += ic[i][k] * tmp[8*k+j];
	block[8*i+j] =  s >> 15;
	
      } /* end of i */

    } /* end of j */
#endif
  }
}

void Initialize_Fast_IDCT()
{
  int i, j;
  double s;

#if 0
  iclp = iclip+512;
  for (i= -512; i<512; i++)
    iclp[i] = (i<-256) ? -256 : ((i>255) ? 255 : i);
#endif

  
  for (j=0; j<8; j++) {
    for (i=0; i<8; i++) {
      s = (i==0) ? sqrt(0.125) : 0.5;
      
      ic[j][i] = (short) ((s * cos((PI/8.0)*i*(j+0.5)) * 32768) + 0.5); 
    }
  }
}
