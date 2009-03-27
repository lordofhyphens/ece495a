//#ifndef USART_UTIL
//#define USART_UTIL
/** 
	Prototypes and definitions for code dealing with the management
	of the USART interface of AVR 8515 microcontrollers.
**/
#include "usart_baud.inc"
void usart_init(); 
void usart_close();
void usart_set_baud_rate();

//#endif
