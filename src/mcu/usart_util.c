#include <avr/io.h>

void uart_init (void) {
	UCSRB |= (1 << RXEN) | (1 << TXEN); 
	// Turn on the transmission and reception circuitry
	UCSRC |= (1 << URSEL) | (1 << UCSZ0) | (1 << UCSZ1); // Use 8-bit character sizes

	UBRRL = BAUD_PRESCALE; // Load lower 8-bits of the baud rate value into the low byte of the UBRR register
	UBRRH = (BAUD_PRESCALE >> 8); // Load upper 8-bits of the baud rate value into the high byte of the UBRR register
}

// initialize the I/O ports we'll be using. Might not actually necessary 
void io_init(void) {
	// Set PORTC to input, and PORTD6 and PORTD7 to input
	DDRC = 0;
	DDRD6 = 0;
	DDRD7 = 0;
}

