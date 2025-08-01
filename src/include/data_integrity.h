#ifndef DATA_INTEGRITY_H
#define DATA_INTEGRITY_H

#define MAX_BUFFER_SIZE 128

int safe_copy(unsigned char *dest, const unsigned char *src, int max_length);

#endif