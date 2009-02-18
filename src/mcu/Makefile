# Set our compiler to the AVR-specific GCC compiler
CC=avr-gcc
# Set the architecture, 
# see http://www.nongnu.org/avr-libc/user-manual/using_tools.html
# for a list.
#MCU=atmega16
MCU=atmega8515

# CPU Frequency in Hz (so freq in MHz * 10^6). 
F_CPU='F_CPU=18432000'
# Optimization level 
OPTI_LEVEL=s
# Putting it all together for the compiler.
FLAGS=-Wall -mmcu=$(MCU) -D$(F_CPU) -g -O$(OPTI_LEVEL)

all: 
	$(CC) usart.c $(FLAGS)
