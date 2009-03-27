#include <avr/io.h>
#include <stdio.h>
#include "usart_util.h"

void usart_init (void) {
	UCSRB |= (1 << RXEN) | (1 << TXEN); 
	// Turn on the transmission and reception circuitry
	UCSRC |= (1 << URSEL) | (1 << UCSZ0) | (1 << UCSZ1); // Use 8-bit character sizes

	UBRRL = BAUD_PRESCALE; // Load lower 8-bits of the baud rate value into the low byte of the UBRR register
	UBRRH = (BAUD_PRESCALE >> 8); // Load upper 8-bits of the baud rate value into the high byte of the UBRR register
}


