/*******
* usart.c - simple code for communication over a serial link.
* Written by Joseph Lenox, derived in part from code available at
* http://www.nongnu.org/avr-libc/user-manual/group__stdiodemo.html
*
*/
#include <avr/io.h>
#include <stdio.h>
#define USART_BAUDRATE 921600
#define BAUD_PRESCALE ((F_CPU / (USART_BAUDRATE * 16)) - 1)

// This needs to be after the defines because the utils use them.
#include "usart_util.h"

int main(void) {
	// Set up the uart.
	unsigned char ByteToSend;
	unsigned char bufferByte;
	unsigned char zero = 0;
	unsigned int n = 0;
	uart_init();
	io_init();

	// TODO: Allow us to start and stop the loop, based on a given input port.
	// Probably will involve some tri-stating of the USART transmit/receive.

	//Set up the first two bytes to send.
	ByteToSend = PORTC;
	bufferByte = ((1 >> PORTD7) | PORTD6);
	// Loop forever !
	while (1) {
		// Wait for the buffer to clear before filling it more.
		while ((UCSRA & (1 << UDRE)) == 0) {}; 
		UDR = ByteToSend;
		n++;
		if (n > 4) { n = 0; }
		// the 2*n multiplier on the shift is because of the leftover bits when doing a 10->8 adaptation.
		ByteToSend = bufferByte |= ((2*n) >> PORTC);
		bufferByte = zero; // clear the buffer between writes
		if (n!=0) {
			/* Set the buffer to the proper amount of shift. 
			   the branch should actually be unnecessary.
			*/
			bufferByte = (unsigned int)((2*n) << PORTC) | (2*n) >> PORTD6 | (((2*n)+1) >> PORTD7);
		} else {
			bufferByte = (1 >> PORTD7) | PORTD6;
		}
	}
	return 0;
}
