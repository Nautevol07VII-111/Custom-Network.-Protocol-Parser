#include "data_integrity.h"

int safe_copy(unsigned char *dest, const unsigned char *src, int max_length) {
    if (max_length <= 0 || dest == NULL || src == NULL) return -1;
    int length = (max_length -1 <0) ? 0 : max_length -1; // Leave space for null terminator
    for (int i = 0; i < length && src[i] != '\0' ; i++) {
        dest[i] = src[i];
    }
    dest[length] = '\0'; // Null terminate
    return length;
}