	; VEC_TRANSP_MULT
	; Loads two streams (one steam for each column)

BEGIN 0 
	vld8:8:16:1  r9, r0, v0         ; load only 32 doubles as stream core
	vld8:8:16:1  r10, r0, v0        ; load only 32 doubles as stream core
       	sadd8  r0, r0, s4 		; keep sum in s4

END

	; VEC_TRANSP_MULT+1
	; Do the multiplication for two double
	; VEC_TRANSP_MULT: Note we do not put sum store at end of this loop
	; since they are negligible. Also, s4 has to be reduced at 
	; end of the loop
BEGIN 1
		   
	smul8    v0, v1, s0   ; multiply two doubles from V0 and V1
	sadd8    s0, s4, s4   ; keep sum in s4

	; this should really be  vcinc:2:2:0  v0, v1, r0
	; but to emulate a stream, we do not increment counter
	;
	vcinc:0:0:0  r0, r0, r0 
END


 	; SIMD_TRANSP_MULT: Note we do not put sum init, sum store, or
	; reduction of two doubles at the end of loop since they are negligible
BEGIN 3

	   sld8    r9, r0, s0   ; load two doubles from A_col_i to s0
	   sld8   r10, r0, s4   ; load two doubles from B_col_j to s4
	   smult  s0,  s4, s8   ; multiply
	   sadd   s8, s12, s12  ; s12 = sum

END