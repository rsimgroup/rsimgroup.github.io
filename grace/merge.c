#include <stdio.h>
#include <time.h>

#define INSERT_TOP "<!-- STRIP_TOP -->"
#define INSERT_BOT "<!-- STRIP_BOTTOM -->"
#define DATE_TOP "<!-- DATE -->"

main(int argc, char *argv[])
{
  int state;

  char buf[32];
  char date[128];
  char *name;

  time_t timeval;

  int copy = 1;

  int c;

  char *in_line[1024];

  FILE *template, *input;

  template = fopen(argv[1],"r");
  input = fopen(argv[2],"r");

  if( argc > 3 )
    name = argv[3];
  else
    name = "Daniel Grobe Sachs";

  time(&timeval);
  sprintf(date,"This page was last modified by %s on %s",name,asctime(localtime(&timeval)));

  memset(buf,32,32);

  while( !feof(template) )
  {
    memmove(buf,buf+1,31);
    c = getc(template);
    if( copy && (c!=EOF) ) putchar(c);

    buf[31]=c;

    if( memcmp(INSERT_TOP,buf+(32-strlen(INSERT_TOP)),strlen(INSERT_TOP)) == 0 ) 
    {
      copy = 0;
  
      while( (c = getc(input)) != EOF )
	putchar(c);
    }

    if( memcmp(INSERT_BOT,buf+(32-strlen(INSERT_BOT)),strlen(INSERT_BOT)) == 0 ) 
    {
       copy = 1;
    }

    if( memcmp(DATE_TOP,buf+(32-strlen(DATE_TOP)),strlen(DATE_TOP)) == 0 ) 
       puts(date);

  }
}
