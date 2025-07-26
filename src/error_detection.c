#include "error_detection.h"

unsigned char calculate_checksum(const unsigned char *data, int length) {
    unsigned char checksum = 0; 
    for (int i = 0; i < length; i++) {
        checksum ^= data[i];
    }
    return checksum;
}