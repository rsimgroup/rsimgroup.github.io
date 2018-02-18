	;; SIMD_FDCT ported from INTEL SSE

	;; FDCT COL
	;; r9 is block, r10 tg_all_16, r11 one_corr
BEGIN X
	sld2	r9+16, r0, s0
	sld2	r9+96, r0, s4
	sadd2	s0, r0, s8
	sld2	r9+32, r0, s12
	sadd2	s0, s4, s0
	sld2	r9+80, , s16
	sshl	s0, i2, s0
	sld2	r9, r0, s20
	sadd2	s16, s12, s16
	sld2	r9+112, r0, s24
	sadd2	s20, s24, s20
	sshl	s16, i2, s16
	sadd2	s0, r0, s24
	ssub2	s8, s4, s8
	ssub2	s0, s16, s0
	sld2	r9+48, r0, s28
	sld2	r9+64, r0, s4
	sadd2	s28, s4, s28	
	sld2	r10+16, r0, s4
	smul2	s4, s0, s4
	sshl2	s20, i2, s20
	sadd2	s24, s16, s24
	sshl2	s28, i2, s28
	sadd2	s20, r0, s16
	ssub2	s20, s28, s20
	sadd2	s4, s20, s4
	sadd2	s16, s28, s16
	sld2	r11, r0, s28
	sor2	s4, s28, s4
	sld2	r10+16, r0, s28
	sshl	s8, i3, s8
	smul2	s20, s28, s20
	sadd2	s16, r0, s28
	ssub2	s20, s0, s20
	sld2	r9+80, r0, s0
	ssub2	s12, s0, s12
	ssub2	s16, s24, s16
	sst2	s4, r0, r9+32
	sadd2	s28, s24, s28
	sadd2	s24, r0, s28
	sld2	r9+64, r0, s24
	sld2	r9+48, r0, s4
	sshl	s12, i3, s12
	ssub2	s4, s24, s4
	sadd2	s8, r0, s24
	sst2	s16, r0, r9+64
	sld2	r10+64, r0, s16
	sadd2	s8, s12, s8
	smul2	s8, s16, s8
	ssub2	s24, s12, s24
	smul2	s24, s16, s24
	sst2	s28, r0, r9
	sld2	r11, r0, s16
	ssub2	s20, s0, s20
	sor2	s20, s16, s20
	sshl2	s4, i2, s4
	sor2	s8, s16, s8
	sadd2	s4, r0, s16
	sld2	r9, r0, s12
	sld2	r9+112, r0, s28
	sadd2	s4, s24, s4
	ssub2	s12, s28, s12
	ssub2	s16, s24, s16
	sld2	r10, r0, s0
	sshl2	s12, i2, s12
	sst2	r9+96, r0, s20
	sld2	r10+32, r0, s20
	smul2	s0, s4, s0
	smul2	s20, s16, s24
	ssub2	s12, s8, s28
	sadd2	s12, s8, s12
	smul2	s20, s28, s20
	sadd2	s0, s12, s0
	sadd2	s24, s16, s24
	sadd2	s20, s28, s20
	sadd2	s20, s16, s20
	sld2	r10, r0, s16
	smul2	s12, s16, s12
	sld2	r11, r0, s16
	sor2	s0, s16, s0
	ssub2	s28, s24, s28
	sst2	s0, r0, r9+16
	sst2	s28, r0, r9+48
	ssub2	s12, s4, s12
	sst2	s20, r0, r9+80
	sst2	s12, r0, r9+112
END

	;; FDCT ROW
	;; r9 is block, r10 is TABLE, r11 is round_frw_row
BEGIN X+1
	sld2	r9, r0, s0
	sld2	r9+8, r0, s4

	sor2	s8, s8, s8
	sshufl4 s0, i68, s0
	sshufl2 s4, i27, s4
	ssub2	s8, s4, s8
	sunpk8	s4, s8, s4
	sadd2	s0, s4, s0
	sshufl2	s0, i216, s0
	sshufl4	s0, i0, s4
	sld2	r10, r0, r8
	smulad2 s4, s8, s4
	sshufl4	s0, i85, s8
	sshufh2 s0, i216, s0
	sshufl4	s0, i170, s12
	sld2	r10+32, r0, s16
	sld2	r10+16, r0, s20
	sld2	r11, r0, s24
	sld2	r10+48, r0, s28
	smulad2	s12, s16, s12
	smulad2	s8, s20, s8
	sadd2	s4, s24, s4
	sadd2	s12, s24, s12
	sshufl4	s0, i255, s0
	smulad2	s0, s28, s0

	sadd2	s4, s8, s4
	sadd2	s0, s12, s0

	sshr4	s4, i15, s4
	sshr4	s0, i15, s0

	sadd2	s4, r0, s8
	sunpk4	s4, s0, s4
	sunpk4	s8, s0, s8
	spak2	s4, s8, s4
	sshr2	s4, i4, s4
	sst2	s4, r0, r9

END