#include <stdio.h>
#include "command_processing.h"

void process_command(const unsigned char *command, in length) {
    if (length >= 6 && strncmp((char *)command, "LED_ON", 6) == 0) {
        printf("LED turned ON\n");
    } else if (length >= 7 && strncmp((char *)command, "LED_OFF", 7) == 0) {
        printf("LED turned OFF\n");
    } else {
        printf("Unknown command\n");
    }
}

void simulate_sensor_reading(float *value) {
    *value = 25.5; // Simulated temperatue reading
}