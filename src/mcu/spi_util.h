/*
 * SPI interface code library.
 * Adapted from ATMEGA8515 datasheet.
 */
#ifndef SPI_UTIL_H
#define SPI_UTIL_H

// Change these defines to match the pins that will
// be used for SPI communication.
#define DD_MOSI PINB5
#define DDR_MOSI PORTB5
#define DD_MISO PINB6
#define DDR_MISO PORTB6
#define DD_SCK PINB7
#define DDR_SCK PORTB7
#define DD_SS PINB4
#define DDR_SS PORTB4

// Ifdefs are for minimizing code in a given binary.
#ifdef SPI_MASTER
void SPI_Master_Init(); 
// Wait for transmit to complete unless you are only sending one byte and are
// sure it won't happen again.
void SPI_Master_Transmit(char cData, int wait_for_transmit);
#endif

#ifdef SPI_SLAVE
void SPI_Slave_Init();
char SPI_Slave_Receive();
#endif

#endif
