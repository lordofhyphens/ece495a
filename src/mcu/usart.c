/*******
* usart.c - simple code for communication over a serial link.
* Written by Joseph Lenox, derived in part from code available at
* http://www.nongnu.org/avr-libc/user-manual/group__stdiodemo.html
*
*/
#include <inttypes.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include <util/delay.h>
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
unsigned char pack_usart(volatile uint8_t port1,volatile uint8_t port2);
int main(void) {
	// Set up the uart.
	volatile unsigned char command;
	usart_init();
	io_init();
	// set up the SPI.
	SPI_Master_Init();

	// TODO: Allow us to start and stop the loop, based on a given input port.
	// Probably will involve some tri-stating of the USART transmit/receive.

	// Wait for the USART recieve buffer to get a command for the device.
	while (!(UCSRA & (1<<RXC))) {;}
	command = UDR;

	SREG = 0x80;

	SPI_Master_Transmit(command, 1);
	
	// Loop forever !
	while (1) {
		while ((UCSRA & (1 << UDRE)) == 0) {};
		UDR = pack_usart(PINC, (PIND & 0xA0));
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
	unsigned volatile char sel = (PINA & 0x0F);
	send_bt_command((PGM_P)pgm_read_word(&(wt32_commands[sel])));
}
ISR(INT1_vect) 
{
	unsigned volatile char sel = (PINA & 0x0F);
	if (sel == WT32_RESET) {
		// Reset the WT32 manually.
		PORTD = PORTD | (1 << PORTD5);
		_delay_ms(50);
		PORTD = PORTD & ~(1 << PORTD5);
	}
}
// initialize the I/O ports we'll be using.
void io_init(void) {
	char volatile tmp; 
	// Set PORTC to input, and PORTD6 and PORTD7 to input
	DDRC = 0;
	PORTC = 0xFF;
	DDRD = 0x22; // all but D5 and D1 as inputs.
	PORTD = 0xCD; // pull-up resistors.
	// Set PORTB2 to input, pull up resistor.
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
void send_bt_command(PGM_P cmd) {
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
	for (i = 0; i < strlen_P(cmd); i++) {
		while ((UCSRA & (1 << UDRE)) == 0) {}; 
		UDR = cmd[i];
	}
	// Wait for a response.	
	_delay_ms(60);
	// Go back to data mode.
	while ((PINB & WT_DATA_MODE) == 0) {
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

unsigned char pack_usart(volatile uint8_t port1,volatile uint8_t port2) {
	static unsigned char buffer = 0x00;
	unsigned char outp = 0x00;
	static unsigned int n = 0;
	if (n > 4) { n = 0;}
	switch (n) {
		case 0:	outp = (port1 >> 2) | port2;
			buffer = port1 << 6;
			break;
		case 1:
			outp = (buffer | port2 >> 2 | port1 >> 4);
			buffer = (port1 << 4);
			break;
		case 2:
			outp = (buffer | port2 >> 4 | port1 >> 6);
			buffer = (port1 << 2);
			break;
		case 3:	
			outp = (buffer | port2 >> 6);
			buffer = port1;
			break;
		case 4:
			outp = buffer;
			buffer = 0x00;
			break;
	}
	n++;
	return outp;
}
