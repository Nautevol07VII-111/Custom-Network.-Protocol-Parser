#ifndef PROTOCOL_H
#define PROTOCOL_H

// Define packet structure (like a network packet an Arduino might send)
typedef struct {
    unsigned char start_byte; 
    unsigned char length;     
    unsigned char payload[32]; 
    unsigned char checksum;   
    unsigned char end_byte;   
} Packet;

//Constants
#define START_BYTE 0xAA
#define END_BYTE 0xBB
#define MAX_PAYLOAD 32


//declaring functions
void create_packet(Packet *packet, unsigned char length);
int parse_packet(Packet *packet);

#endif