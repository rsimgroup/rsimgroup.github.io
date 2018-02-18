#include <stdio.h>
#include <time.h>

#define INSERT_TOP "<!-- STRIP_TOP -->"
#define INSERT_BOT "<!-- STRIP_BOTTOM -->"

main(int argc, char *argv[])
{
  int state;

  char buf[32];
  char date[128];
  char *name;

  time_t timeval;

  int copy = 0;

  int c;

  char *in_line[1024];

  FILE *template, *input;

  template = fopen(argv[1],"r");

  memset(buf,32,32);

  while( !feof(template) )
  {
    memmove(buf,buf+1,31);
    c = getc(template);
    if( copy && (c!=EOF) ) putchar(c);

    buf[31]=c;

    if( memcmp(INSERT_TOP,buf+(32-strlen(INSERT_TOP)),strlen(INSERT_TOP)) == 0 ) 
    {
      copy = 1;
    }

    if( memcmp(INSERT_BOT,buf+(32-strlen(INSERT_BOT)),strlen(INSERT_BOT)) == 0 ) 
       copy = 0;

  }
}
