#!/usr/bin/perl

$mpgd_sse = "/home/sasanka/tmp/alex_testing/Face_rec_SSE/execs/face_project_sse";

$mpgd_nosse ="/home/sasanka/tmp/alex_testing/Face_rec_SSE/execs/face_project_nosse";

$args = " -outfile dist.dat -lastphase -infile 00001aa.sfi -imDir data/csuScrapShots/normSep2002sfi train/scraps/feretPCA.train imagelists/new_scrap_all.srt Face MahCosine";

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

