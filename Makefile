CC = gcc
CFLAGS = Iinclude -Wall -g 
OBJECTS = src/main.o src/error_detection.o src/protocol_validation.o src/command_processing.o src/data_integrity.o 

protocol_parser: $(OBJECTS)
$(CC) $(OBJECTS) -o protocol_parser 

%.o: %.c 
     $(CC) $(CFLAGS) -c $< -o $@

clean: 
     rm -f src/*.o protocol_parser