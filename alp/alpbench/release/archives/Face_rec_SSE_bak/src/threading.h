#include<pthread.h>
#include "csuCommon.h"

typedef struct barrier_struct {
  int padding1[8]; /* Padding bytes to avoid false sharing and cache aliasing */
  pthread_mutex_t lock;   /* Mutex lock for the structure */
  int n_clients;          /* Number of threads to wait for at barrier */
  int n_waiting;          /* Number of currently waiting threads */
  int phase;              /* Flag to separate waiters from fast workers */
  pthread_cond_t wait_cv; /* Clients wait on condition variable to proceed */
  int padding2[8]; /* Padding bytes to avoid false sharing and cache aliasing */
} barrier_t;

typedef struct {
  int id;
  Matrix images, subspims;
  Subspace* s;
} thrd_args_t;

barrier_t * thread_barrier_init(int n_clients);
void thread_barrier_destroy(barrier_t *barrier);
void thread_barrier(int t,barrier_t *barrier);

Matrix thrd_centerthenproject(Subspace *s, Matrix images);

