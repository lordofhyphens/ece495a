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
