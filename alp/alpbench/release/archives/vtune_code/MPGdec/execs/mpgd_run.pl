#!/usr/bin/perl

$mpgd_sse = "/home/adve_s/sasanka/alex/release/vtune_code/MPGdec/execs/mpeg2dec_sse";

$mpgd_nosse ="/home/adve_s/sasanka/alex/release/vtune_code/MPGdec/execs/mpeg2dec_nosse";

$args = " -b /home/adve_s/manlapli/more_space/release/MPGenc/execs/blah.m2v -f -o0 hello -q";

for ($i=0; $i<10;$i++) {
  system($mpgd_nosse.$args);
  system("gprof ".$mpgd_nosse. " > nosse".$i);
  system($mpgd_sse.$args);
  system("gprof ".$mpgd_sse. " > sse".$i);
}

