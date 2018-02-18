#include <stdio.h>

int main (int argc, char**argv) 
{
  int start_num = atoi(argv[1]);
  char* fn = argv[2];
  FILE* infile;
  char str[100];
  int blah[4];
  char *sp, dig[3];

  infile = fopen(fn, "r");
  dig[2]='\0';
  while(!feof(infile)) {
    fscanf(infile, "%s %d %d %d %d\n", str, &blah[0],&blah[1],&blah[2],&blah[3]);
    sp = str;
    sp[5]+=start_num;
    if (sp[5] > '9') {
      sp[5]-=10;
      sp[4]='1';
    }
#if 1
    str[2]='0';
    printf("%s %d %d %d %d\n", &str[2], blah[0],blah[1],blah[2],blah[3]);
#else
    printf("%s %d %d %d %d\n", &str[0], blah[0],blah[1],blah[2],blah[3]);

#endif    
  };
}
