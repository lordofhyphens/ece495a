/*******
* usart.c - simple code for communication over a serial link.
* Written by Joseph Lenox, derived in part from code available at
* http://www.nongnu.org/avr-libc/user-manual/group__stdiodemo.html
*
*/
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

// This needs to be after the defines because the utils use them.
#include "spi_util.h"
#include "usart_util.h"
#include "control_defines.h"
#include "usart.h"

int main(void) {
	// Set up the uart.
	unsigned char ByteToSend;
	unsigned char bufferByte;
	unsigned char command;
	unsigned char zero = 0;
	unsigned int n = 0;
	usart_init();
	io_init();
	// set up the SPI.
	SPI_Master_Init();

	// TODO: Allow us to start and stop the loop, based on a given input port.
	// Probably will involve some tri-stating of the USART transmit/receive.

	// Wait for the USART recieve buffer to get a command for the device.
	while (!(UCSRA & (1<<RXC))) {;}
	command = UDR;

	SPI_Master_Transmit(command, 1);

	//Set up the first two bytes to send.
	ByteToSend = PINC;
	bufferByte = (PIND & 0xA0) >> 6;
	
	// Loop forever !
	while (1) {
		// Wait for the buffer to clear before filling it more.
		while ((UCSRA & (1 << UDRE)) == 0) {}; 
		UDR = ByteToSend;
		n++;
		if (n > 4) { n = 0; }
		// the 2*n multiplier on the shift is because of the leftover bits when doing a 10->8 adaptation.
		ByteToSend = bufferByte |= (PINC << (2*n));
		bufferByte = zero; // clear the buffer between writes
		if (n!=0) {
			/* Set the buffer to the proper amount of shift. 
			   the branch should actually be unnecessary.
			*/
			bufferByte = (unsigned char)(PINC << (2*n)) | (PIND & 0xA0) << (2*n);
//			bufferByte = (unsigned int)(PINC << (2*n)) | (2*n) >> PORTD6 | (((2*n)+1) >> PORTD7);
		} else {
			bufferByte = (PIND & 0xA0) >> 6;
		}
	}
	return 0;
}

// Recieve a new command for the device, which requires
// that we be in the WT32 data mode.
ISR(UART_RX_vect) 
{
	if ((PIND & WT_DATA_MODE) != 0) {
		char command;
		// Just to be sure, wait to make sure we're good to go.
		while (!(UCSRA & (1<<RXC))) {;}
		command = UDR;
		SPI_Master_Transmit(command, 1);
	}
}
// initialize the I/O ports we'll be using.
void io_init(void) {
	char tmp; 
	// Set PORTC to input, and PORTD6 and PORTD7 to input
	DDRC = 0;
	PORTC = 0xFF;
	DDRD = (1<<PORTD6) | (1<<PORTD7);
	PORTD = 0xA0;

	// Set PORTE0 to input with pull-up

	// set the interrupts behavior
	tmp = MCUCR & 0xF0; 
	MCUCR = tmp | 0x0F;

	// enable all three interrupts.
	tmp = GICR & 0x1F;
	GICR = tmp | 0xE0;
}

void send_bt_command(char* cmd) {
	int i;
	delay_s(1);	
	for (i = 0; i < 3; i++) {
		while ((UCSRA & (1 << UDRE)) == 0) {}; 
		UDR = '+';
	}
	delay_s(1);	
	
	for (i = 0; i < strlen(cmd); i++) {
		while ((UCSRA & (1 << UDRE)) == 0) {}; 
		UDR = cmd[i];
	}
}

void delay_s(int t) {
	int i;
	TCCR0 = 5;
	TCNT0 = 0;
	TIFR = (1 << TOV0);
	for (i = 0; i < t * (F_CPU / 1024); i++) {
		while ((TIFR & 1) != 1) {}
	}
	
}
