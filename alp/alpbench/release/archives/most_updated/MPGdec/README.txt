Authors
=======
Alex Li (manlapli@uiuc.edu)
Ruchira Sasanka (sasanka@uiuc.edu)


Parallelization of MPEG2 decoder
================================

This encoder is a modified version of the MSSG MPEG2 decoder. The original 
version can be found at http://www.mpeg.org/MSSG/#source. Details of the base
decoder can be found in README, ARCHITECTURE, and m2d_old.doc. This document 
focuses on the modifications of the decoder.

Parallelization
---------------

POSIX threads are used to parallelize the MPEG2 decoder. The parallelization 
uses a fork-join model for every frame, i.e., forking out different threads at 
the beginning of the bitstream processing and joining all threads after segments
of the frame are reconstructed from the bitstream.

Since the bitstream is inherently serial, the main thread first indentifies the 
slices (a line of macroblocks in a frame that can be decoded independently) from
the bitstream and then distributes equal number of slices to different threads.
Thus, each thread is responsible for a specific part of the frame (e.g. top half
and bottom half). The main thread copies the slices into the private buffers of 
the threads so that decoding can be carried out independently. The slice 
distribution and multithreading initiation are done in new_slice function in 
getpic.c. After the slice is processed (i.e. Entropy decoding, IDCT, and 
iQuant), each thread writes to the corresponding part in the frame buffer. 
Then, all threads are joined and the main thread outputs the reconstructed 
frame.

As the original version is single-thread, most of the functions are written 
assuming a single buffer. In order to enable parallel processing of the 
bitstream, many of the functions are modified to access the private buffers of
different threads. These functions are prefixed with Thrd_, e.g. 
Thrd_decode_macroblock.

