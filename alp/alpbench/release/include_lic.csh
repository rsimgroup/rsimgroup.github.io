#!/usr/csh

foreach fn (*.c *.h)
cat ../../LICENSE.txt $fn > tmp
cat tmp > $fn
end
rm tmp

