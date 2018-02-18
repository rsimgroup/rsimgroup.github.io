Authors
=======
Alex Li (manlapli@uiuc.edu)
Ruchira Sasanka (sasanka@uiuc.edu)


Parallelization of MPEG2 encoder
================================

This encoder is a modified version of the MSSG MPEG2 encoder. The original 
version can be found at http://www.mpeg.org/MSSG/#source. Details of the base
encoder can be found in README, ARCHITECTURE, and mpeg2enc.doc. This document 
focuses on the modifications of the encoder.

The differences between the current version and the base version are

1) 3-step motion search instead of full search, and 
2) parallelized processing of the frames.


3-step Motion Search
--------------------

The 3-step search algorithm is written by Eric Debes. Its implementation can be 
found in the fullsearch function in motion.c. A high-level description of the 3 
steps taken is followed.

1) Calculate the distance of the center block.
2) If the result from step 1 exceeds the preset threshold, calculate the 
distances between the matching block and the blocks in the search window. Mark
the one with minimum error. The blocks are 4 pels apart.
3) Search around the blocks that are next to the center block. More 
specifically, the eight surrounding blocks that are 2 pels away from the center
block.

This search algorithm greatly reduces the computations when comparing with 
traditional full search algorithm. 


Parallelization
---------------

POSIX threads are used to parallelize the MPEG2 encoder. The parallelization 
uses a fork-join model for every frame, i.e., forking out different threads at 
the beginning of the frame processing and joining all threads before the frame 
is written to the bitstream. 

The multithreading is initiated in the thread_work_dist() function in putseq.c.
The frame is partitioned statically among different threads, i.e., for 2 
threads, thread 0 takes the top half and thread 1 takes the bottom half of the
frame. The needed parameters are then passed to individual threads so that
motion estimation, DCT, quantization, IDCT, inverse quantization, and entropy 
coding can be done in parallel. The threaded functions are prefixed with pt,
e.g., ptmotion_estimation. 

While quantization depends on the bit rate in the original encoder, the 
current encoder uses a fix quantization value to allow threads to perform 
independent operations. This results in variable bit rate bitstream. However,
current implementations of MPEG2 decoder can handle VBR encoding and thus it
is not a big issue.

To create the bitstream, each thread is given a buffer to write its encoded
frame segment. After thread join is encountered, the main thread combines
all the segments into one bitstream.


