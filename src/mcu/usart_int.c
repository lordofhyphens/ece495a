#include <avr/interrupt.h>

ISR(INT0_vect) 
{
	// Code for INT0 pin interrupt.
}
ISR(INT1_vect)
{
	// Code to deal with the INT1 interrupt
}
ISR(INT2_vect)
{
	// deal with the INT2 interrupt, which is "general command" mode
	// Check the status of Port A0-A3, and perform an action based on that.
}
