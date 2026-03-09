# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Makefile for Embedded C apps
CC = clang
CXX = clang++
CFLAGS = -Wall -Wextra -O2

# Using standard libraries (libc), no external dependencies.
# This ensures easy compilation on FreeBSD.

SRCS = src/sensor_reader.c src/telemetry_daemon.c src/security_monitor.c
BINS = $(SRCS:src/%.c=%)

all: $(BINS)

sensor_reader: src/sensor_reader.c
	$(CC) $(CFLAGS) -o $@ $<

telemetry_daemon: src/telemetry_daemon.c
	$(CC) $(CFLAGS) -o $@ $<

security_monitor: src/security_monitor.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(BINS)
