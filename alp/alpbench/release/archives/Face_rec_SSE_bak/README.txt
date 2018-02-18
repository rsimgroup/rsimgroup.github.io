Authors
=======
Alex Li (manlapli@uiuc.edu)
Ruchira Sasanka (sasanka@uiuc.edu)


Parallelization of CSU Face Recognition system
==============================================

The current recognizer is a subset of the CSU face recognition algorithm 
evaluation system. The original version can be found at 
http://www.cs.colostate.edu/evalfacerec/. Details of the base version can be 
found in README and faceIdUsersGuide.pdf. This document focuses on the 
modifications made to the base version.

This version focuses on the Eigen face PCA algorithm. To compile the necessary
binaries, do

1) make preprocess
2) make subspace
3) make -f makefile_sp

In the main directory, run './scripts/runPCA_PP_Train_scraps.sh' and the scrap
images included in this package are preprocessed and trained. One can also 
download the FERET database to test on larger number of images.

To compute distances, run './scripts/PCAproject.sh' which the 2nd pass compute
distances in MahCosine between the probe image with the given image list.

Parallelization
---------------

POSIX threads are used to parallelize the application in  3 different occasions

1) projecting the gallery images onto the trained subspace,
2) projecting the probe image onto the subspace, and
3) distance calculation of the probe iamge against gallery images.

The first event can be done once offline before the application is run. Images 
are divided evenly among threads to project onto the subspace. Threads are
created in readAndProjectImages function in csuCommonSubspace.c.

The second event occurs when a probe image is given and to be aligned to the
trained subspace. Threads divide up the large subspace during projection of
the probe image, which is essentially a matrix multiply. The threading is 
initiated in transposeMultiplyMatrixL function of csuCommonMatrix.c.

The third event occurs when the distances between the probe image and the
gallery images are to be calculated. Threads evenly divide up the gallery
images and perform distance computations. In the current version, only
MahCosine is implemented since it gives good accuracy and performance
trade-off among the other algorithms. The thread creation is done in
computeOneDistances function in csuSubspaceProject.c.