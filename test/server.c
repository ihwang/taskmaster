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
    int clilen;
    struct data mydata;
    struct sockaddr_un clientaddr, serveraddr;

    sockfd = socket(PF_LOCAL, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        perror("socket error : ");
        exit(1);
    }
    unlink(argv[1]);

    bzero(&serveraddr, sizeof(serveraddr));
    bzero(&clientaddr, sizeof(clientaddr));
    serveraddr.sun_family = PF_LOCAL;
    clientaddr.sun_family = PF_LOCAL;
    strcpy(serveraddr.sun_path, argv[1]);
    strcpy(clientaddr.sun_path, argv[2]);

    if (bind(sockfd, (struct sockaddr*)&serveraddr, sizeof(serveraddr)) < 0)
    {
        perror("bind error : ");
        exit(1);
    }
    clilen = sizeof(clientaddr);

    while (1)
    {
        if ((recvfrom(sockfd, (void*)&mydata, sizeof(mydata), 0, (struct sockaddr*)&clientaddr, (socklen_t*)&clilen)) > 0)
        {
            printf("%d + %d = %d\n", mydata.a, mydata.b, mydata.a + mydata.b);
            sendto(sockfd, (void*)&mydata, sizeof(mydata), 0, (struct sockaddr*)&clientaddr, clilen);
        }
    }
    close(sockfd);
    exit(0);
}