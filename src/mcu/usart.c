/*******
* usart.c - simple code for communication over a serial link.
* Written by Joseph Lenox, derived in part from code available at
* http://www.nongnu.org/avr-libc/user-manual/group__stdiodemo.html
*
*/
#define USART_BAUDRATE 921600
#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16)) - 1)

#include <avr/io.h>

// Set up the USART interface with our desired baud rate.
void usart_init(void) {
	UBRRL = BAUD_PRESCALE;

	// This enables both transmit and recieve.
	UCSRB = _BV(TXEN) | _BV(RXEN);
}
