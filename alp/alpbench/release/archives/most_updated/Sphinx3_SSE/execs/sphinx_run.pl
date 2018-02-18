#!/usr/bin/perl

$mpgd_sse = "/home/sasanka/tmp/alex_testing/Sphinx3_SSE/execs/livepretend_sse";


$mpgd_nosse ="/home/sasanka/tmp/alex_testing/Sphinx3_SSE/execs/livepretend_nosse";

$args = " ./model/lm/an4/an4.ctl ./model/lm/an4 ./model/lm/an4/args.an4 >& an4.log";

for ($i=0; $i<4;$i++) {
  system($mpgd_nosse.$args);
  system("gprof ".$mpgd_nosse. " > nosse".$i);
  system("cp gmon.out gmon_nosse".$i);
}

for ($i=0; $i<4;$i++){
  system($mpgd_sse.$args);
  system("gprof ".$mpgd_sse. " > sse".$i);
  system("cp gmon.out gmon_sse".$i);
}

