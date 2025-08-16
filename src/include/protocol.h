#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <stdint.h>

// Binary packet structure
typedef struct {
    unsigned char start_byte;
    unsigned char length;
    unsigned char payload[32];
    unsigned char checksum;
    unsigned char end_byte;
} Packet;

// Constants
#define START_BYTE 0xAA
#define END_BYTE 0xBB
#define MAX_PAYLOAD 32
#define MAX_BUFFER_SIZE 64

// Text protocol functions
int is_valid_text_protocol(const unsigned char *data, int length);
int extract_command(const unsigned char *data, int length, char *command);

// Binary packet functions
void create_packet(Packet *packet, const char *command);
int text_to_binary(const char *text_command, Packet *packet);
void print_packet(const Packet *packet);
unsigned char calculate_checksum(const Packet *packet);

#endif