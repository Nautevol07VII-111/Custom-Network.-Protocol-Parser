#include "error_detection.h"

unsigned char calculate_checksum(const unsigned char *data, int length) {
    unsigned char checksum = 0; 
    for (int i = 0; i < length; i++) {
        checksum ^= data[i];
    }
    return checksum;
} 

int verify_checksum(const unsigned char *data, int length, unsigned char expected_checksum) {
    unsigned char computed_checksum = calculate_checksum(data, length);
    return computed_checksum == expected_checksum;
}