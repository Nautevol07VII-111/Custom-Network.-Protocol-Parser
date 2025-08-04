#include <stdio.h>
#include <string.h>
#include "../include/protocol.h"
#include "error_detection.h"
#include "protocol_validation.h"
#include "command_processing.h"
#include "data_integrity.h"

int main() {
    unsigned char buffer[MAX_BUFFER_SIZE] = "<LED_ON>abc";
    int buffer_length;
    unsigned char checksum;

    while(1) {
        printf("Enter command (e.g., <LED_ON> or <q> to quit):");
        if (fgets((char *)buffer, MAX_BUFFER_SIZE, stdin) == NULL) break;
        buffer_length = strlen((char *)buffer);
        if (buffer_length > 0 && buffer[buffer_length -1] == '\n') buffer_length--;

        if (buffer_length == 1 && buffer[0] == 'q') break; //Quit condition
    
        checksum = calculate_checksum(buffer + 1, buffer_length -2); //computes checksum for validation

    if (is_valid_protocol(buffer, buffer_length)) {
        printf("Protocol is valid\n");
        if (verify_checksum(buffer + 1, buffer_length -2, checksum 2)) {
        unsigned char command[MAX_BUFFER_SIZE];
        safe_copy(command, buffer_length -2);
        process_command(command, buffer_length -2);
    } else {
        printf("Checksum failed\n");
    }
} else {
    printf("Invalid protocol\n");
    }
 }
float sensor_value;
simulate_sensor_reading(&sensor_value);
printf("Simulated sensor reading: %.1f\n", sensor_value);


return 0;
}

