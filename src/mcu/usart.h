/** 
	Prototypes and definitions for code dealing with the management
	of the USART interface of AVR 8515 microcontrollers.
**/
#ifndef USART_H
#define USART_H

#define USART_BAUDRATE 921600
#define BAUD_PRESCALE ((F_CPU / (USART_BAUDRATE * 16)) - 1)

void usart_init(); 
void usart_close(); 
void usart_set_baud_rate(); 

#endif
