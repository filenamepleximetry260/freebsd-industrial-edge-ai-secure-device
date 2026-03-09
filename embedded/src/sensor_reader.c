/*
 * LICENSE UPL
 * Author: Mauro Risonho de Paula Assumpção
 * Description: C implementation of sensor_reader
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define SENSOR_FILE "/tmp/sensor_data.txt"

int main() {
    float temperature = 40.0;
    float vibration = 2.0;
    float current = 8.0;

    printf("Starting sensor_reader...\n");

    while (1) {
        // Try to read from simulator file, if it exists
        FILE *f = fopen(SENSOR_FILE, "r");
        if (f) {
            fscanf(f, "temperature=%f vibration=%f current=%f", &temperature, &vibration, &current);
            fclose(f);
        } else {
            // Simulate normal operation if no simulator file
            temperature = 40.0 + ((float)rand() / (float)RAND_MAX) * 2.0 - 1.0;
            vibration = 2.0 + ((float)rand() / (float)RAND_MAX) * 0.2 - 0.1;
            current = 8.0 + ((float)rand() / (float)RAND_MAX) * 0.5 - 0.25;
        }

        // Output JSON telemetry pattern
        printf("{\"device_id\":\"edge-arm64\",\"temperature\":%.2f,\"vibration\":%.2f,\"current\":%.2f,\"timestamp\":%ld}\n",
               temperature, vibration, current, time(NULL));
        fflush(stdout);

        sleep(1);
    }

    return 0;
}
