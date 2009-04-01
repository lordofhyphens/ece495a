/** 
	main_control.c - datapath control logic.
	From the schematic:
	PORTC3-7 - Control lines 0-4
	PORTD7 - Control line 5

	two lowest-order bits are the "General" bits. 
**/

#include "main_control.h"
#include "control_util.h"
#include "control_defines.h"
#define SPI_SLAVE 1
#include "spi_util.h"

void mcu_pin_init();

int main(void) {
	// inp - the raw data from the user. 
	// opc - opcode of this given command (lowest 2 bits).
	// cmd - the high end bits, used to define either a datapath
	//       or specific input configurations.
	char inp, opc, cmd;

	// given operation flags. 
	char flags;
	// Starting initializiations.
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
		}
		if ((opc & OPC_INPUT) != 0) {
			// cmd is for periphial configuration.
			// Pin C3 = LSB, Pin D7 = MSB. 
			// This makes for weird assignments and bit operations.
			PORTC = ;
		}
		
		// wait for a new command from the user.
		inp = SPI_Slave_Receive();
	}
	return 0;
}

void mcu_pin_init() {
	// set pins C3-C7 to output
	DDRC = (1<<DDC3) | (1<<DDC4) | (1<<DDC5) | (1<<DDC6) | (1<<DDC7);
	DDRD = (1<<DDD7);
	_NOP();
}
