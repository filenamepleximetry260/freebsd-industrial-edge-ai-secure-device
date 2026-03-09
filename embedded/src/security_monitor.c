/*
 * LICENSE UPL
 * Author: Mauro Risonho de Paula Assumpção
 * Description: C implementation of security_monitor
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 1024

// Very basic rule-based security monitor
// Checks JSON strings for values that are anomalous based on hardcoded rules.

int main() {
    char buffer[BUFFER_SIZE];
    
    printf("Starting security_monitor (Rule-based validation)...\n");

    while (fgets(buffer, BUFFER_SIZE, stdin) != NULL) {
        // Output the data so it can be chained
        printf("%s", buffer);
        fflush(stdout);

        // Simple substring parsing to extract values (Not robust JSON parsing for simplicity)
        char *temp_ptr = strstr(buffer, "\"temperature\":");
        if (temp_ptr) {
            float temp = atof(temp_ptr + 14);
            if (temp > 80.0) {
                fprintf(stderr, "[SECURITY_ALERT] Edge anomaly detected: High Temperature (%.2f)\n", temp);
            }
        }
        
        char *vib_ptr = strstr(buffer, "\"vibration\":");
        if (vib_ptr) {
            float vib = atof(vib_ptr + 12);
            if (vib > 10.0) {
                fprintf(stderr, "[SECURITY_ALERT] Edge anomaly detected: High Vibration (%.2f)\n", vib);
            }
        }
    }

    return 0;
}
