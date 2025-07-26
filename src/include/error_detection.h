#ifndef ERROR_DETECTION_H
#define ERROR_DETECTION_H 

unsigned char calculate_checksum(const unsigned char *data, int length);
int verify_checksum(const unsigned char *data, int length, unsigned char expected_checksum);


#endif