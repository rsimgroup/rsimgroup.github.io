Authors
=======
Alex Li (manlapli@uiuc.edu)
Ruchira Sasanka (sasanka@uiuc.edu)


Parallelization of CMU Sphinx 3-0.1 Speech Recognizer
=====================================================

The current recognizer is a subset of the CMU Sphinx 3-0.1. The original version
can be found at http://cmusphinx.sourceforge.net/html/cmusphinx.php. Details of
the base version can be found in README and the doc directory. This document 
focuses on the modifications made to the base version.

This release is a stripped down version of the original version and the 
directory hierarchy has also been changed. This version produces the livepretend
binaries that takes in an audio sample and attempts to translate the speech 
sample into text. 

To compile, type 'make' at the main directory. The makefile includes comments
that explain the different options in this release.

To test the program, first modify $HOME in sphinx3-test to point to the main 
directory. Then, at the main directory, do './scripts/sphinx3-test' and the
sample P I T T S B U R G H should be recognized. If a big endian machine is
used to run the program, change the file name in model/lm/an4/an4.ctl to
pittsburgh.bigendian.

Parallelization
---------------

Three phases are parallelized in the Sphinx 3-0.1 program. The threading.c file 
contains all the multithreaded code used in the parallelization. The three
phases are

1) Gaussian model scoring,
2) Lexical tree node evaluation, and
3) Lexical tree node propagation.

POSIX threads are used to divide the workload. The multithreading initiation is
called at the utt_decode_block function in utt.c. The actual thread creations 
are carried out at thrd_scoring_phase function in threading.c. The threading
model adopts the fork-barrier-join model. Threads encounter a barrier after 
each parallel phase and wait until the next parallel phase starts. After the
last parallel phase, the threads are joined.

In Gaussian model scoring phase, threads evenly divide the large number of 
senones and calculate the Mahalanobis distance between the feature vector and 
the given Gaussian model.

Lextree nodes are activated based on the senone scores generated from phase one.
In lextree node evaluation, the active nodes in the lextree are evenly divided
among threads so that HMM scores are evaluated in all the active HMM models.

In lextree node propagation, the active nodes are evenly divided among threads
so that the next iteration's active nodes are collectively generated based on
the scores generated from the last phase.

