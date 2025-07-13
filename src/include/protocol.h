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