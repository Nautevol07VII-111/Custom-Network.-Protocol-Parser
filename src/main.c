#include <stdio.h>
#include <string.h>
#include "../include/protocol.h"

//gets the sum of payload from byte array
unsigned char calculate_checksum(unsigned char *data, unsigned char length) {
    unsigned char sum = 0;
    for (int i = 0; i < length; i++) {
        sum += data[i];
    }
    return sum;
}

void create_packet(Packet *packet, unsigned char *data, unsigned char length) {
    if (length > MAX_PAYLOAD) {
        printf("Error: Payload too large\n");
        return;
    }
    packet->start_byte = START_BYTE;
    packet->length = length;
    memcpy(packet->payload, data, length); //copies data to payload
    packet->checksum = calculate_checksum(data, length);
    packet->end_byte = END_BYTE;
}

int parse_packet(Packet *packet) {
    if (packet->start_byte != START_BYTE || packet->end_byte != END_BYTE) {
        printf("Error: Invalid start or end byte\n");
        return -1;
    }
    if (packet->length > MAX_PAYLOAD) {
        printf("Error: Invalid length\n");
        return -1;
    }
    unsigned char calc_checksum calculate_checksum(packet->payload, packet->length);
    if (calc_checksum != packet->checksum) {
        printf("Error: Checksum mismatch\n");
        return -1;
    }
    return 0; //no error found;condition met
}

int main() {
    //Simulates sending a packet
    Packet packet; //creating a new instance of the packet object(struct) from the protocol.h file
    unsigned char data[] = {0x01, 0x02, 0x03}; // Example data
    create_packet(&packet, data, 3);
}