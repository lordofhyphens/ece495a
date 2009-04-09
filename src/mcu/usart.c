/*******
* usart.c - simple code for communication over a serial link.
* Written by Joseph Lenox, derived in part from code available at
* http://www.nongnu.org/avr-libc/user-manual/group__stdiodemo.html
*
*/
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include <util/delay.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
// This needs to be after the defines because the utils use them.
#include "spi_util.h"
#include "usart_util.h"
#include "control_defines.h"
#include "usart.h"

char wt32_command_0[] PROGMEM = "A";
char wt32_command_1[] PROGMEM = "B";
char wt32_command_2[] PROGMEM = "C";
char wt32_command_3[] PROGMEM = "D";
char wt32_command_4[] PROGMEM = "E";
char wt32_command_5[] PROGMEM = "F";
char wt32_command_6[] PROGMEM = "G";
char wt32_command_7[] PROGMEM = "H";
char wt32_command_8[] PROGMEM = "I";
char wt32_command_9[] PROGMEM = "J";
char wt32_command_A[] PROGMEM = "K";
char wt32_command_B[] PROGMEM = "L";
char wt32_command_C[] PROGMEM = "M";
char wt32_command_D[] PROGMEM = "N";
char wt32_command_E[] PROGMEM = "O";
char wt32_command_F[] PROGMEM = "P";

PGM_P wt32_commands[] PROGMEM = {
	wt32_command_0,
	wt32_command_1,
	wt32_command_2,
	wt32_command_3,
	wt32_command_4,
	wt32_command_5,
	wt32_command_6,
	wt32_command_7,
	wt32_command_8,
	wt32_command_9,
	wt32_command_A,
	wt32_command_B,
	wt32_command_C,
	wt32_command_D,
	wt32_command_E,
	wt32_command_F
};

int main(void) {
	// Set up the uart.
	unsigned char ByteToSend;
	unsigned char c, d;
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
		c = PINC;
		d = (PIND & 0xA0) >> 6;
		ByteToSend = bufferByte | (c << (2*n));
		bufferByte = zero; // clear the buffer between writes
		if (n!=0) {
			/* Set the buffer to the proper amount of shift. 
			   the branch should actually be unnecessary.
			*/
			bufferByte = (unsigned char)(c >> (2*(4-n))) | d << (2*n);
		} else {
			bufferByte = d;
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
// Send a command to the WT32 itself. 
ISR(INT0_vect)
{
	// check the status of PINA0-A3
	unsigned char sel = (PINA & 0x0F);
	char* buf;
	// copy the proper string out of our special string table in program space.
	buf = malloc((sizeof(char)*strlen_P((PGM_P)pgm_read_word(&(wt32_commands[sel]))))+1);
	strcpy_P(buf, (PGM_P)pgm_read_word(&(wt32_commands[sel])));
	send_bt_command(buf);
	free(buf);
}

// initialize the I/O ports we'll be using.
void io_init(void) {
	char tmp; 
	// Set PORTC to input, and PORTD6 and PORTD7 to input
	DDRC = 0;
	PORTC = 0xFF;
	DDRD = (1<<PORTD6) | (1<<PORTD7);
	PORTD = 0xA0;
	// Set PORTB2 to input
	PORTB = PORTB | (1<<PORTB2);
	// Set PORTE0 to input with pull-up
	PORTE = (1 << PORTE0);
	// set the interrupts behavior
	tmp = MCUCR & 0xF0; 
	MCUCR = tmp | 0x0F;

	// enable all three interrupts.
	tmp = GICR & 0x1F;
	GICR = tmp | 0xE0;
}
// Function to send an actual BT command to the RS232 system, given a specific string. 
void send_bt_command(char* cmd) {
	int i;
	while ((PIND & WT_DATA_MODE) != 0) {
		delay_s(1);	
		for (i = 0; i < 3; i++) {
			while ((UCSRA & (1 << UDRE)) == 0) {}; 
			UDR = '+';
		}
		delay_s(1);	
	}	
	// Send the command itself
	for (i = 0; i < strlen(cmd); i++) {
		while ((UCSRA & (1 << UDRE)) == 0) {}; 
		UDR = cmd[i];
	}
	// Wait for a response.	
	_delay_ms(60);
	// Go back to data mode.
	while ((PIND & WT_DATA_MODE) == 0) {
		delay_s(1);	
		for (i = 0; i < 3; i++) {
			while ((UCSRA & (1 << UDRE)) == 0) {}; 
			UDR = '+';
		}
		delay_s(1);
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

