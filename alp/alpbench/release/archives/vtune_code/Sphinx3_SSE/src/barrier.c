#include <stdlib.h>
#include "barrier.h"

barrier_t * thread_barrier_init(int n_clients) {
  barrier_t *barrier = (barrier_t *) malloc(sizeof(barrier_t));

  if (barrier != NULL) {
    barrier->n_clients = n_clients;
    barrier->n_waiting = 0;
    barrier->phase = 0;
    pthread_mutex_init(&barrier->lock, NULL);
    pthread_cond_init(&barrier->wait_cv, NULL);
  }

  return barrier;
}

void thread_barrier_destroy(barrier_t *barrier) {
  pthread_mutex_destroy(&barrier->lock);
  pthread_cond_destroy(&barrier->wait_cv);
  free(barrier);
}

void thread_barrier(int t, barrier_t *barrier) {
#if (NUM_THREADS>1)
  int my_phase;

  pthread_mutex_lock(&barrier->lock);
  my_phase = barrier->phase;
  barrier->n_waiting++;

  if (barrier->n_waiting == barrier->n_clients) {
    barrier->n_waiting = 0;
    barrier->phase = 1 - my_phase;
    pthread_cond_broadcast(&barrier->wait_cv);
  }
#if 0
  printf("thrd %d bp %d mp %d waiting %d\n",t, barrier->phase, my_phase, barrier->n_waiting);
#endif
  while (barrier->phase == my_phase) {
    pthread_cond_wait(&barrier->wait_cv, &barrier->lock);
  }

  pthread_mutex_unlock(&barrier->lock);
#endif
}
