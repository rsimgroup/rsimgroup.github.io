/* fdctref.c, forward discrete cosine transform, double precision           */

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

#include <math.h>

#include "config.h"
#include "global.h"

#ifndef PI
# ifdef M_PI
#  define PI M_PI
# else
#  define PI 3.14159265358979323846
# endif
#endif

/* global declarations */
void init_fdct _ANSI_ARGS_((void));
void fdct _ANSI_ARGS_((short *block));

/* private data */
#ifndef INT_DCT
static double c[8][8]; /* transform coefficients */
#endif


void init_fdct()
{
  int i, j;
  double s;

  for (i=0; i<8; i++)
  {
    s = (i==0) ? sqrt(0.125) : 0.5;

    for (j=0; j<8; j++){

#ifdef INT_DCT
      /* scaled with 2^15*/
      c[i][j] = (short) ((s * cos((PI/8.0)*i*(j+0.5)) * 32768) + 0.5); 
      ic[j][i] = c[i][j];
#else
      c[i][j] = s * cos((PI/8.0)*i*(j+0.5));
#endif
    }
      
  }
}


#ifdef INT_DCT
void fdct(block)
short *block;
{
  short tmp[64];

#ifdef SSE2

   short *b_p, *cp, *tmp_p, *b2_p;

    /* not the most elegant approach, can be improved with other fast DCT 
       methods out there */
    
    b_p = block;/*block+8*i;*/
    cp = &c[0][0];
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
	  mov   edx, [cp]       ; /*load ic ptr */
	  mov   eax, [tmp_p]    ;
      
	idct_row_loop:
	  movdqu   xmm0, [ebx]      ; /*load 8 shorts from block*/
	  movdqu   xmm1, [edx]         ; /*ic[0][0..7]*/
	  movdqu   xmm2, [edx+16]      ; /*ic[1][0..7]*/
	  movdqu   xmm3, [edx+32]      ; /*ic[2][0..7]*/
	  movdqu   xmm4, [edx+48]      ; /*ic[3][0..7]*/

	  movdqu   xmm7, [edx+64]      ; /*ic[4][0..7]*/

	  pmaddwd xmm1, xmm0     ; /* xmms : 4 32-bit partial sums */
	  pmaddwd xmm2, xmm0     ;
	  pmaddwd xmm3, xmm0     ;
	  pmaddwd xmm4, xmm0     ;
	  pmaddwd xmm7, xmm0     ;

	  movdqa  xmm5, xmm1     ;
	  movdqa  xmm6, xmm3     ;

	  unpcklpd xmm1, xmm2    ; /*xmm1: 2.1 2.0 1.1 1.0 */
	  unpckhpd xmm5, xmm2    ; /*xmm5: 2.3 2.2 1.3 1.2 */

	  movdqu   xmm2, [edx+80]      ; /*ic[5][0..7]*/

	  unpcklpd xmm3, xmm4    ;
	  unpckhpd xmm6, xmm4    ;

	  movdqu   xmm4, [edx+96]      ; /*ic[6][0..7]*/
	  pmaddwd  xmm2, xmm0    ;

	  paddd  xmm6, xmm3      ; 

	  movdqu   xmm3, [edx+112]      ; /*ic[7][0..7]*/
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

	  movdqu [eax], xmm1     ;

	  add   ebx, 16         ;
	  add   eax, 16         ;

	  cmp   ebx, ecx        ;
	  jb    idct_row_loop   ;
	  
	}
    /* This is second phase */
    __asm 
      {
	mov edx, [tmp_p]        ; /* load tmp blk ptr */
	mov eax, [cp]          ; /* load coeffs table ptr*/
	mov ebx, [b_p]          ;
	mov edi, [b2_p]         ;

      idct_col_outer:
	movdqu xmm6, [eax]      ; /* load ic[0][0..7] */
	
	pxor xmm4, xmm4         ;
	pxor xmm5, xmm5         ;
	mov  ecx, 8             ;

      idct_col_loop:
	movdqu xmm1, [edx]      ; /* load tmp[0][0..7] */
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

	movdqu [ebx], xmm5    ; /*store to block[i][j]*/

	add  ebx, 16          ;
	add  eax, 16          ;
	cmp  ebx, edi         ;
	jb   idct_col_outer   ;
      }

#else /* NON-SSE2 code */

  int i, j, k;
  int s;
  short tmp[64];
  for (i=0; i<8; i++) { 

 
    for (j=0; j<8; j++) { 


      s = 0;
      for (k=0; k<8; k++)
        s += c[j][k] * block[8*i+k];          /* this is block[i][k] */

      tmp[8*i+j] = s >> 15;                         /* this is block[i][j] */
    }
  }
  for (j=0; j<8; j++) {

    for (i=0; i<8; i++) {

      s = 0;

      for (k=0; k<8; k++)
        s += c[i][k] * tmp[8*k+j];

      block[8*i+j] =  s >> 15;

    } /* end of i */
    
    
  } /* end of j */
#endif
}
#else /* NOT INT_DCT */

void fdct(block)
short *block;
{

  double s;
  double tmp[64];


  for (i=0; i<8; i++) { 

 
    for (j=0; j<8; j++) { 

      s = 0.0;
      for (k=0; k<8; k++)
        s += c[j][k] * block[8*i+k];          /* this is block[i][k] */
      tmp[8*i+j] = s;

    }  /* for j */
  

  } /* for i */


  for (j=0; j<8; j++) {

    for (i=0; i<8; i++) {

      s = 0.0;

      for (k=0; k<8; k++)
        s += c[i][k] * tmp[8*k+j];

      block[8*i+j] = (int)floor(s+0.499999);

      /*
       * reason for adding 0.499999 instead of 0.5:
       * s is quite often x.5 (at least for i and/or j = 0 or 4)
       * and setting the rounding threshold exactly to 0.5 leads to an
       * extremely high arithmetic implementation dependency of the result;
       * s being between x.5 and x.500001 (which is now incorrectly rounded
       * downwards instead of upwards) is assumed to occur less often
       * (if at all)
       */

    } /* end of i */


  } /* end of j */



}

#endif


