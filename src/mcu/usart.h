/** 
	Prototypes and definitions for code dealing with the management
	of the USART interface of AVR 8515 microcontrollers.
**/

// if we pass in a baud rate from the makefile, don't override it.
#ifndef USART_BAUDRATE
#define USART_BAUDRATE 921600
#endif
#ifndef BAUD_PRESCALE
#define BAUD_PRESCALE ((F_CPU / (USART_BAUDRATE * 16)) - 1)
#endif
void io_init();
void delay_s(int);
void send_bt_command(char*);
