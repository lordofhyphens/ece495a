# Set our compiler to the AVR-specific GCC compiler
CC=avr-gcc
# Set the architecture, 
# see http://www.nongnu.org/avr-libc/user-manual/using_tools.html
# for a list.
#MCU=atmega16
MCU=atmega8515
UTILS=spi_util.o usart_util.o 
USART_OBJECTS=usart.o  
CONT_OBJECTS=main_control.o 

# CPU Frequency in Hz (so freq in MHz * 10^6). 
# F_CPU='F_CPU=18432000'
# using internal oscillator, comment out if not using.
F_CPU='F_CPU=8000000'
# Desired baud rate for our USART.
USART_BAUD='USART_BAUDRATE=115200'
# Optimization level 
OPTI_LEVEL=s
# Putting it all together for the compiler.
FLAGS=-Wall -mmcu=$(MCU) -D$(F_CPU) -D$(USART_BAUD) -O$(OPTI_LEVEL) -funsigned-char

all: $(UTILS) $(USART_OBJECTS) $(CONT_OBJECTS)
	$(CC) -o usart_c.o $(USART_OBJECTS) $(UTILS)
	${CC} -o main_c.o $(UTILS) $(CONT_OBJECTS)
bin: usart_c.o main_c.o
	avr-objcopy --output-target binary main_c.o main_c.bin
	avr-objcopy --output-target binary usart_c.o usart_c.bin
debug: $(UTILS) $(USART_OBJECTS) $(CONT_OBJECTS)
	$(CC) -g -o usart_c.o $(USART_OBJECTS) $(UTILS)
	${CC} -g -o main_c.o $(UTILS) $(CONT_OBJECTS)
asm: $(UTILS) $(USART_OBJECTS) $(CONT_OBJECTS)
	$(CC) -o usart_c.o $(USART_OBJECTS) $(UTILS)
	${CC} -o main_c.o $(UTILS) $(CONT_OBJECTS)
	avr-objdump -zhD main_c.o > main_c.od
	avr-objdump -zhD usart_c.o > usart_c.od
usart : $(USART_OBJECTS) $(UTILS)
	$(CC) $(FLAGS) $(UTILS) $(USART_OBJECTS) -o usart_c.o 
main : $(CONT_OBJECTS) $(UTILS)
	${CC} -o mainc.o $(UTILS) $(CONT_OBJECTS)

$(UTILS): $(UTILS:.o=.h) $(UTILS:.o=.c)
	$(CC) $(FLAGS) -c $(UTILS:.o=.c)

$(CONT_OBJECTS): $(CONT_OBJECTS:.o=.h) $(UTILS)
	$(CC) $(FLAGS) -c $(CONT_OBJECTS:.o=.c)

$(USART_OBJECTS): $(USART_OBJECTS:.o=.h) $(USART_OBJECTS:.o=.c) usart.h $(UTILS)
	$(CC) $(FLAGS) -c $(USART_OBJECTS:.o=.c)

clean:
	rm -f *.o *.s *.od

