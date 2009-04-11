/** 
	main_control.c - datapath control logic.
	From the schematic:
	PORTC3-7 - Control lines 0-4
	PORTD7 - Control line 5

	two lowest-order bits are the "General" bits. 
**/

#include "main_control.h"
#include "control_defines.h"
#define SPI_SLAVE 1
#include "spi_util.h"
#include <avr/io.h>
#include <util/delay.h>

int main(void) {
	// inp - the raw data from the user. 
	// opc - opcode of this given command (lowest 2 bits).
	// cmd - the high end bits, used to define either a datapath
	//       or specific input configurations.
	unsigned volatile char inp, opc, cmd;
	unsigned volatile char buf, mask;
	opc = 0;
	inp = 0;
	cmd = 0;
	buf = 0;
	mask = 0;


	// Starting initializiations.
	SPI_Slave_Init();
	mcu_pin_init();

	// Get the initial configuration from the other controller.	
	inp = SPI_Slave_Receive();
	// loop forever for now, we'll use an interrupt to reset.
	while(1) {
		// Decode the command.
		opc = inp & MCU_OPCODE;
		cmd = ((inp & MCU_COMMAND) >> 2); // right shift to keep everything in lowest
		if (opc == OPC_DATAP) {
			// cmd is for datapath configuration
			buf = cmd & 0x1F;
			mask = PORTC & 0x07; // save the first five bits of PORTC.
			PORTC = decode_datapath_code(cmd, PINC);
		}
		if (opc == OPC_INPUT) {
			buf = cmd & 0x1F;
			mask = PORTC & 7; // save the last three bits of PORTC.
			// cmd is for periphial configuration.
			// Pin C3 = LSB, Pin D7 = MSB. 
			// This makes for weird assignments and bit operations.
			// Don't touch port c0-c2, so we need to be careful.
			PORTC = (buf << 3) | mask;
			PORTD = (cmd >> 5) ^ PORTD;
			_delay_ms(5);
			//_NOP(); // need to find this function
		}
		if (opc == OPC_USART) {
			PORTA = send_usart_command(cmd);
			// set our configuration ports
			// set the interrupt high that we're using for BT commands.
			PORTA = PORTA | (1 << PORTA2);
			// delay for a short time.
			_delay_ms(100);
			// reset the interrupt to low.
			PORTA = PORTA & ~(1 << PORTA2);
		}
		
		// wait for a new command from the user.
		inp = SPI_Slave_Receive();
	}
	return 0;
}

void mcu_pin_init() {
	// set all of PORTC to output
	DDRC = 0xFF;
	DDRD = (1<<PORTD7);
	// Set PORTA to output.
	DDRA = 0xFF;
	// PortB is being handled by SPI_slave_init()
	// _NOP(); // need to find this.
}

// MCU_*_ON values are in control_defines.h
unsigned char decode_datapath_code(char command, char port) {
	volatile char outp = port;
	if ((command & MCU_ANALOG_ON)   != 0) { 
		outp = outp | MCU_ANALOG_ON;
	} else { 
		outp = outp & ~(MCU_ANALOG_ON);
	}
	if ((command & MCU_DIGITAL_ON)  != 0) { 
		outp = outp | MCU_DIGITAL_ON;
	} else {
		outp = outp & ~(MCU_DIGITAL_ON);
	}
	if ((command & MCU_OUTPUT_ON) != 0) { 
		outp = outp | MCU_OUTPUT_ON;
	} else {
		outp = outp & ~(MCU_OUTPUT_ON);
	}
	return outp;
}

unsigned char send_usart_command(unsigned char cmd) {
	// clear the low
	unsigned volatile char old_set = PORTA;
	// check to make sure cmd is in the left side.
	if ((cmd & 0xF0) != 0) {
	} else { 
		cmd = (cmd << 4);
	}
	// Clear, set, and then assign.
	old_set = old_set & 0x0F;
	old_set = old_set | cmd;
	return old_set;
}

/* I2C software implementation on port C7 and D7
   Adapted from http://www.robot-electronics.co.uk/htm/using_the_i2c_bus.htm
   This should probably be broken out into its own source file.
*/
void i2c_start() {
	// C7 is SDA
	PORTC = _BV(PORTC7);
	_delay_us(1);
	// D7 is SCL
	PORTD = _BV(PORTD7);
	_delay_us(1);

	PORTC = (unsigned char)PORTC & (unsigned char)~_BV(PORTC7);
	_delay_us(1);
	PORTD = (unsigned char)PORTD & (unsigned char)~_BV(PORTD7);
}

void i2c_stop() {
	PORTC = (unsigned char)PORTC & (unsigned char)~_BV(PORTC7);
	_delay_us(1);
	PORTD = _BV(PORTD7);
	_delay_us(1);
	PORTC = _BV(PORTC7);
	_delay_us(1);
}

unsigned char i2c_rx(char ack) {
	
	char x, d=0;
	PORTC = _BV(PORTC7);

	for(x=0; x<8; x++) {
		d <<= 1;
		do {
			PORTD = _BV(PORTD7);
		} while((PINC & 0xF0)==0);    // wait for any SCL clock stretching
		_delay_us(1);
		if((PINC & 0xF0)) { d |= 1; }
		PORTD = (unsigned char)PORTD & (unsigned char)~_BV(PORTD7);
	} 

	if(ack) {
		PORTC = (unsigned char)PORTC & (unsigned char)~_BV(PORTC7);
	} else {
		PORTC = _BV(PORTC7);
	}
	
	PORTD = _BV(PORTD7);
	_delay_us(1);             // send (N)ACK bit
	PORTD = (unsigned char)PORTD & (unsigned char)~_BV(PORTD7);
	return d;
}

unsigned char i2c_tx(unsigned char d) {
	char x;
	static unsigned char b;
	for(x=8; x; x--) {
		if (d & 0x80) {
			PORTC = _BV(PORTC7); 
		} else {
			PORTC = (unsigned char)PORTC & (unsigned char)~_BV(PORTC7);
		}
		PORTD = _BV(PORTD7);
		d <<= 1;
		PORTD = (unsigned char)PORTD & (unsigned char)~_BV(PORTD7);
		_delay_us(10); // guarantee less than 100Khz
	}
	PORTC = _BV(PORTC7);
  	PORTD = _BV(PORTD7);
	_delay_us(1);
	b = (PIND & 0x80) >> 7; // possible ACK bit
	PORTD = (unsigned char)PORTD & (unsigned char)~_BV(PORTD7);
	return b;
}

