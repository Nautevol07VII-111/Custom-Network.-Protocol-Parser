#include <stdio.h>
#include <string.h>
#include "../include/protocol.h"
#include "error_detection.h"
#include "protocol_validation.h"
#include "command_processing.h"
#include "data_integrity.h"

int main() {
    unsigned char buffer[MAX_BUFFER_SIZE] = "<LED_ON>abc";
    int buffer_length = 8;
    unsigned char checksum = 0xAA; //Example expected checksum

    if (is_valid_protocol(buffer, buffer_length)) {
        printf("Protocol is valid\n");
        if (verify_checksum(buffer + 1, buffer_length -2, checksum 2)) {
        unsigned char command[MAX_BUFFER_SIZE];
        safe_copy(command, buffer_length -2);
    } else {
        printf("Checksum failed\n");
    }
} else {
    printf("Invalid protocol\n");
}
float sensor_value;
simulate_sensor_reading(&sensor_value);
printf("Simulated sensor reading: %.1f\n", sensor_value);


return 0;
}

