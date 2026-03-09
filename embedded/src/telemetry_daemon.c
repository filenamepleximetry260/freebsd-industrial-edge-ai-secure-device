/*
 * LICENSE UPL
 * Author: Mauro Risonho de Paula Assumpção
 * Description: C implementation of telemetry_daemon
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define SERVER_IP "10.0.2.2" // QEMU Host IP
#define SERVER_PORT 8080
#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    char *server_ip = SERVER_IP;
    if (argc > 1) {
        server_ip = argv[1];
    }

    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE] = {0};

    printf("Starting telemetry_daemon (Target: %s:%d)...\n", server_ip, SERVER_PORT);

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(SERVER_PORT);

    if (inet_pton(AF_INET, server_ip, &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    // Try connecting in a loop
    while (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("Connection to %s:%d failed. Retrying in 5 seconds...\n", server_ip, SERVER_PORT);
        sleep(5);
    }
    printf("Connected to telemetry server.\n");

    // Read from standard input (expected to be piped from sensor_reader)
    while (fgets(buffer, BUFFER_SIZE, stdin) != NULL) {
        send(sock, buffer, strlen(buffer), 0);
    }

    close(sock);
    return 0;
}
