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


#if 0
  int pid;


  pid = fork();


  if (pid == 0) {  /* for child */
    routine(arg);
    exit(0);
  }
#endif


  return status;



}


int rt_thread_join(rt_thread_t thr, void ** stat) {
  int status=0;  


  return status;
}  





rt_barrier_t * rt_thread_barrier_init(int n_clients) {
  return NULL;
}

void rt_thread_barrier_destroy(rt_barrier_t *barrier) {
}

int rt_thread_barrier(rt_barrier_t *barrier, int increment) {
  return 0;
}






