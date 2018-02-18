	;; IDCT ROW taken from INTEL
	
BEGIN X
	;; r9 is address of block, r10 is addr of coeffs, 
	;; r11 is addr of adjustment const
	
	sld2	r9, r0, s0	; load block line
	sld2	r10, r0, s4	; load coeffs
	sld2	r10+16, r0, s8  ; row 1 of coeffs
	sld2    r10+32, r0, s16 ; row 2 of coeffs
	sld2    r10+48, r0, s24 ; row 2 of coeffs

	sshufl2	s0, i216, s0	; 216=0xd8, switch word 1 and 2 in low half
	sshufh2 s0, i216, s0	; switch 4 and 5 in high half, 0 2 1 3 4 6 5 7

	sshufl4 s0, i0, s20	; s20 is populated with words 0 and 2
	sshufl4 s0, i85, s12	; s12 is populated with words 1 and 3
	sshufl4 s0, i170, s28	; s12 is populated with words 4 and 6
	sshufl4 s0, i255, s0	; s12 is populated with words 5 and 7

	smulad2 s20, s4, s20	; a0 thru a3, parts with x[0] and x[2]
	sld4	r11, r0, s4     ; load in adj const
	smulad2 s12, s8, s12	; b0 thru b3, parts with x[1] and x[3]
	smulad2 s28, s16, s28	; a0 thru a3, parts with x[4] and x[6]
	smulad2 s0, s24, s0	; b0 thru b3, parts with x[5] and x[7]

	sadd4	s20, s28, s20   ; a0 thru a3
	sadd4	s20, s4, s20    ;
	sadd4	s0, s12, s0	; b0 thru a3

	sadd4	s20, s0, s4	; y[0..3]
	ssub4	s20, s0, s0	; y[4..7]
	sshr	s0, i12, s0
	sshr	s4, i12, s4
	spak2	s0, s4, s0
	sst2	s0, r0, r9
END

	;; IDCT COL ported over from INTEL
BEGIN X+1
	;; r9:addr of block, r10:tg_3_16, r11:tg_1_16, r12:tg_2_16, r13:cos_4_16
	;; r14:one_corr, r15:rnd_inv_col, r16:rnd_inv_corr

	sld2	r9+80, r0, s0	; row 5

	sadd2	s0, i0, s8	; from s0 to s2
	
	sld2	r10, r0, s4	; tg_3_16
	sld2	r9+48, r0, s12	; row 3
	sld2	r9+112, r0, s16 ; x7
	smul2	s0, s4, s0	; x5*tg_3_16
	smul2	s4, s12, s4	; x3*tg_3_16
	sld2	r11, r0, s20	; tg_1_16
	
	sadd2	s16, i0, s24

	smul2	s16, s20, s16	; x7*tg_1_16
	sadd2	s0, s8, s0	; x5*tg_3_16+x5 (precision purpose)
	sld2	r9+16, r0, s28	; x1
	smul2	s20, s28, s20	; x1*tg_1_16
	sadd2	s4, s12, s4	; x3*tg_3_16+x3
	sld2	r9+96, r0, s28	; x6
	sadd2	s0, s12, s0	; x3+x5*tg_3_16=tm765
	sld2	r12, r0, s12	; tg_2_16
	ssub2	s8, s4, s8	; x5-x3*tg_3_16=tm465
	smul2	s28, s12, s28	; x6*tg_2_16
	sld2	r9+32, r0, s4	;
	smul2	s12, s4, s12	;
	ssub2	s20, s24, s20	;
	sld2	r9+16, r0, s4	;
	sadd2	s16, s4, s16	; 

	sadd2   s0, i0, s1
	
	sadd2	s0, s16, s0	;
	sub2	s16, s4, s16	;

	sld2	r14, r0, s4	; s1 has one_corr
	sadd2	s0, s4, s0	;
	
	sadd2   s20, i0, s24
	
	sub2	s20, s8, s20
	sadd2	s20, s4, s20
	sadd2	s24, s8, s24
	sst2	s0, r0, r9+112

	sadd2	 s16, i0, s1
	
	sld2	r13, r0, s0
	sadd2	s16, s20, s16	;
	smul2	s0, s16, s8	;
	sst2	s24, r0, r9+48	;
	ssub2	s4, s20, s4	;
	sld2	r9+32, r0, s24	;
	sld2	r9+96, r0, s20	;
	sadd2	s28, s24, s28	;
	ssub2	s12, s20, s12	;
	sld2	r9, r0, s24	;
	smul2	s0, s4, s0	;
	sadd2	s16, s8, s16	;
	sld2	r9+64, r0, s8	;
	sadd2	s8, s24, s20	;
	ssub2	s24, s8, s24	;
	sld2	r14, r0, s8	;
	sor	s16, s8, s16	;
	sadd2	s0, s4, s0	;
	sor	s0, s8, s0	;
	
	sadd2	s20, i0, s8
	sadd2	s20, s28, s20	;
	
	sadd2	s24, i0, s1
	sadd2	s24, s12, s24	;
	ssub2	s4, s12, s4	; 
	sld2	r15, r0, s12	;
	sadd2	s20, s12, s20	;
	ssub2	s8, s28, s8	;
	sld2	r9+112, r0, s28	;
	sadd2	s24, s12, s24	;
	sld2	r16, r0, s12	; 
	sadd2	s28, s20, s28	;
	sshr2	s28, i5, s28	;
	sadd2	s4, s12, s4	;
	sadd2	s8, s12, s8	;
	
	sadd2	s24, i0, s12

	sadd2	s24, s16, s24	;
	sst2	s28, r0, r9	;
	sshr2	s24, i5, s24	;
	sadd2	s4, i0, s28
	sadd2	s4, s0, s4	;
	sst2	s24, r0, r9+16	;
	sshr2	s4, i5, s4	;
	sld2	r9+48, r0, s24	;
	ssub2	s28, s0, s28	;
	sshr2	s28, i5, s28	;
	sst2	s4, r0, r9+32	;
	sld2	r9+112, r0, s4	;
	ssub2	s20, s4, s20	;
	sshr2	s20, i5, s20	;
	sst2	s20, r0, r9+112	;
	ssub2	s12, s16, s12	;
	sld2	r9+48, r0, s16	; 
	sadd2	s24, s8, s24	;
	ssub2	s8, s16, s8	;
	sshr2	s24, i5, s24	;
	sshr2	s8, i5, s8	;
	sst2	s24, r0, r9+48	;
	sshr2	s12, i5, s12	;
	sst2	s8, r0, r9+64	;
	sst2	s28, r0, r9+80	;
	sst2	s12, r0, r9+96	; 

	
END