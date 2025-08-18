#include <string.h>
#include <stdio.h>
#include "protocol.h"

int text_to_binary(const char *text_command, Packet *packet) {
    // Extract command from <COMMAND> format
    int len = strlen(text_command);
    if (len < 3) return 0;
    
    char command[MAX_PAYLOAD];
    int cmd_len = 0;
    
    // Skip < and > markers
    if (text_command[0] == '<' && text_command[len-1] == '>') {
        cmd_len = len - 2;
        if (cmd_len > MAX_PAYLOAD) cmd_len = MAX_PAYLOAD;
        strncpy(command, text_command + 1, cmd_len);
        command[cmd_len] = '\0';
    } else {
        return 0;
    }
    
    
    packet->start_byte = START_BYTE;
    packet->length = cmd_len;
    memset(packet->payload, 0, MAX_PAYLOAD);
    memcpy(packet->payload, command, cmd_len);
    packet->checksum = calculate_checksum(packet);
    packet->end_byte = END_BYTE;
    
    return 1;
}

unsigned char calculate_checksum(const Packet *packet) {
    unsigned char checksum = packet->length;
    for (int i = 0; i < packet->length; i++) {
        checksum ^= packet->payload[i];  
    }
    return checksum;
}

void print_packet(const Packet *packet) {
    printf("\n=== Binary Packet ===\n");
    printf("Start Byte: 0x%02X\n", packet->start_byte);
    printf("Length: %d bytes\n", packet->length);
    printf("Payload (hex): ");
    for (int i = 0; i < packet->length; i++) {
        printf("%02X ", packet->payload[i]);
    }
    printf("\nChecksum: 0x%02X\n", packet->checksum);
    printf("End Byte: 0x%02X\n", packet->end_byte);
    printf("Total Size: %d bytes\n", 5 + MAX_PAYLOAD);
}