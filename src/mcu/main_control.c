/** 
	main_control.c - datapath control logic.
**/

#include "main_control.h"
#include "control_util.h"
#include "control_defines.h"
#define SPI_SLAVE 1
#include "spi_util.h"


int main(void) {
	char cmd;
	// Starting initializiations.
	SPI_Slave_Init();

	// Get the initial configuration from the other controller.	
	cmd = SPI_Slave_Receive();
	// loop forever for now, we'll use an interrupt to reset.
	while(1) {
		
	}
}


