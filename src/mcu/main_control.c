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
	char inp, opc, cmd;

	// given operation flags. 
	char flags;
	// Starting initializiations.
	mcu_pin_init();
	SPI_Slave_Init();

	// Get the initial configuration from the other controller.	
	inp = SPI_Slave_Receive();
	// loop forever for now, we'll use an interrupt to reset.
	while(1) {
		// Decode the command.
		opc = inp & MCU_OPCODE;
		cmd = ((inp & MCU_COMMAND) >> 2); // right shift to keep everything in lowest
		if ((opc & OPC_DATAP) != 0) {
			// cmd is for datapath configuration
			char buf = cmd & 0x1F;
			char mask = PORTC & 7; // save the first five bits of PORTC.
			PORTC = decode_datapath_code(cmd, PORTC);
		}
		if ((opc & OPC_INPUT) != 0) {
			char buf = cmd & 0x1F;
			char mask = PORTC & 7; // save the last three bits of PORTC.
			// cmd is for periphial configuration.
			// Pin C3 = LSB, Pin D7 = MSB. 
			// This makes for weird assignments and bit operations.
			// Don't touch port c0-c2, so we need to be careful.
			PORTC = (~((cmd & 31) ^ (PORTC >> 3)) | mask);
			PORTD = (cmd >> 5) ^ PORTD;
			_delay_ms(5);
			//_NOP(); // need to find this function
		}
		if ((opc & OPC_USART) != 0) {
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
	DDRC = 0xF;
	DDRD = (1<<PORTD7);
	// Set PORTA to output.
	DDRA = 0xF;
	// PortB is being handled by SPI_slave_init()
	// _NOP(); // need to find this.
}

// MCU_*_ON values are in control_defines.h
unsigned char decode_datapath_code(char command, char port) {
	unsigned char outp = port;
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
	unsigned char old_set = PORTA;
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
