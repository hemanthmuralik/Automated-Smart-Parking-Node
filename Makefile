# Makefile for Smart Parking Node
CC = gcc
CFLAGS = -Wall -Wextra -O2 # O2 = Optimize for speed (Important for embedded)
TARGET = parking_node
SRCS = main.c utility.c

all: $(TARGET)

$(TARGET): $(SRCS)
	@echo "Building Embedded Controller..."
	$(CC) $(CFLAGS) -o $(TARGET) $(SRCS)
	@echo "Build Complete: ./$(TARGET)"

clean:
	@echo "Cleaning up..."
	rm -f $(TARGET) *.o
