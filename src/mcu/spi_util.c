/* 
 * SPI Utilities for AVR microcontrollers.
 * The #ifdefs are for minimizing unused code (only one of the AVRs will 
 * actually be a master or slave).
 * Adapted from ATMega8515 datasheet.
 * Written by Joseph Lenox.
 */
#include <avr/io.h>
#include "spi_util.h"

void SPI_Master_Init() {
	// Set the MOSI and SCK as output, everything else input.
	DDRB = (1 << DDR_MOSI) | (1 << DDR_SCK);
	PORTB = PORTB | (1 << PORTB6) | (1 << PORTB4);
	SPCR = (1 << SPE)| (1 << MSTR) | (1 << SPR0);
}
void SPI_Master_Transmit(char cData, int wait_for_transmit) {
	SPDR = cData;
	while(!(SPSR & (1<<SPIF)) && wait_for_transmit); 
}


void SPI_Slave_Init() {
	DDRB = (1 << DDR_MISO);
	PORTB = PORTB | (1 << PORTB7) | (1 << PORTB5) | (1 << PORTB4);
	SPCR = (1 << SPE) | _BV(SPR0); 
}

char SPI_Slave_Receive() {
	// Wait loop for the receive time.
  	while (!(SPSR & (1 << SPIF))) {;}
	return SPDR;
}
