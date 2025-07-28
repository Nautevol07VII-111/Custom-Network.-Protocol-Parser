#include "protocol_validation.h"

int is_valid_protocol(const unsigned char *data, int length) {
    if (length < 2) return 0; // has to at least have start and end markers 
    return (data[0] == '<' && data[length - 1] == '>');
}