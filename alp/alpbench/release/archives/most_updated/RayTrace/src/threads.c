/*
 * threads.c - code for spawning threads on various platforms.
 *
 *  $Id: threads.c,v 1.35 2002/07/03 22:30:25 johns Exp $
 */ 

#include "machine.h"
#include "threads.h"
#include "ui.h"

#ifdef _MSC_VER
#include <windows.h> /* main Win32 APIs and types */
#include <winbase.h> /* system services headers */
#endif

#if defined(SunOS) || defined(Irix) || defined(Linux) || defined(_CRAY) || defined(__osf__) || defined(AIX)
#include<unistd.h>  /* sysconf() headers, used by most systems */
#endif

#if defined(__APPLE__) && defined(THR)
#include <Carbon/Carbon.h> /* Carbon APIs for Multiprocessing */
#endif

#if defined(HPUX)
#include <sys/mpctl.h> /* HP-UX Multiprocessing headers */
#endif


int rt_thread_numprocessors(void) {
  int a=1;

  return a;
}


int rt_thread_setconcurrency(int nthr) {
  int status=0;

  return status;
}

int rt_thread_create(rt_thread_t * thr, void * routine(void *), void * arg) {
  int status=0;

#ifdef THR
#ifdef USEPOSIXTHREADS 
  status = pthread_create(thr, NULL, routine, arg);
#endif 
#endif /* THR */
 
  return status;
}


int rt_thread_join(rt_thread_t thr, void ** stat) {
  int status=0;  

#ifdef THR
#ifdef USEPOSIXTHREADS
  status = pthread_join(thr, stat);
#endif /* USEPOSIXTHREADS */
#endif /* THR */

  return status;
}  


#if !defined(THR)

rt_barrier_t * rt_thread_barrier_init(int n_clients) {
  return NULL;
}

void rt_thread_barrier_destroy(rt_barrier_t *barrier) {
}

int rt_thread_barrier(rt_barrier_t *barrier, int increment) {
  return 0;
}

#else 

#ifdef USEPOSIXTHREADS
rt_barrier_t * rt_thread_barrier_init(int n_clients) {
  rt_barrier_t *barrier = (rt_barrier_t *) malloc(sizeof(rt_barrier_t));

  if (barrier != NULL) {
    barrier->n_clients = n_clients;
    barrier->n_waiting = 0;
    barrier->phase = 0;
    barrier->sum = 0;
    pthread_mutex_init(&barrier->lock, NULL);
    pthread_cond_init(&barrier->wait_cv, NULL);
  }

  return barrier;
}

void rt_thread_barrier_destroy(rt_barrier_t *barrier) {
  pthread_mutex_destroy(&barrier->lock);
  pthread_cond_destroy(&barrier->wait_cv);
  free(barrier);
}

int rt_thread_barrier(rt_barrier_t *barrier, int increment) {
  int my_phase;

  pthread_mutex_lock(&barrier->lock);
  my_phase = barrier->phase;
  barrier->sum += increment;
  barrier->n_waiting++;

  if (barrier->n_waiting == barrier->n_clients) {
    barrier->result = barrier->sum;
    barrier->sum = 0;
    barrier->n_waiting = 0;
    barrier->phase = 1 - my_phase;
    pthread_cond_broadcast(&barrier->wait_cv);
  }

  while (barrier->phase == my_phase) {
    pthread_cond_wait(&barrier->wait_cv, &barrier->lock);
  }

  pthread_mutex_unlock(&barrier->lock);

  return (barrier->result);
}
#endif
#endif /* THR */



