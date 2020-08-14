#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <stdlib.h>

struct data
{
    int a;
    int b;
    int sum;
};

int main(int argc, char **argv)
{
    int sockfd;
    struct sockaddr_un serveraddr, clientaddr;
    int clilen;
    struct data mydata;

    sockfd = socket(PF_LOCAL, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        perror("exit : ");
        exit(1);
    }
    bzero(&serveraddr, sizeof(serveraddr));
    bzero(&clientaddr, sizeof(clientaddr));
    serveraddr.sun_family = PF_LOCAL;
    clientaddr.sun_family = PF_LOCAL;
    strcpy(serveraddr.sun_path, argv[1]);
    strcpy(clientaddr.sun_path, argv[2]);
    clilen = sizeof(serveraddr);

    if (bind(sockfd, (struct sockaddr*)&clientaddr, sizeof(clientaddr)) < 0)
    {
        perror("bind error : ");
        exit(1);
    }
    mydata.a = atoi(argv[3]);
    mydata.b = atoi(argv[4]);
    mydata.sum = 0;

    if (sendto(sockfd, (void*)&mydata, sizeof(mydata), 0, (struct sockaddr*)&serveraddr, clilen) < 0)
    {
        perror("send error : ");
        exit(1);
    }
    
    if (recvfrom(sockfd, (void*)&mydata, sizeof(mydata), 0, (struct sockaddr*)&serveraddr, (socklen_t*)&clilen) < 0)
    {
        perror("recv error : ");
        exit(1);
    }
    printf("result is : %d\n", mydata.sum);

    close(sockfd);
    exit(0);
}