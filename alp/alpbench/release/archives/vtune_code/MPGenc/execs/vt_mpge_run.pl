#!/usr/bin/perl


for ($i=0; $i<10;$i++) {
  system("/opt/intel/vtune/bin/vtl run -a a9");
  system("/opt/intel/vtune/bin/vtl run -a a10");
}

