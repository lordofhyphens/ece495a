//#ifndef USART_UTIL
//#define USART_UTIL
/** 
	Prototypes and definitions for code dealing with the management
	of the USART interface of AVR 8515 microcontrollers.
**/
#ifndef USART_BAUDRATE
#define USART_BAUDRATE 921600
#endif
#ifndef BAUD_PRESCALE
#define BAUD_PRESCALE ((F_CPU / (USART_BAUDRATE * 16)) - 1)
#endif
void usart_init(); 
void usart_close();
void usart_set_baud_rate();

//#endif
