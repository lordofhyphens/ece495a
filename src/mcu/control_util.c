#include <avr/io.h>
#include "control_defines.h"
#include "control_util.h"

void open_data_input(int input) {
	switch (input) {
		case ANALOG_INPUT: 
			if (PORTC2 == INPUT_ON) {
				portc = portc & (0<<PORTC2);
			}
			if (PORTC1 == INPUT_OFF) {
				portc = portc & (1<<PORTC2);
			}
			break;
		case DIGITAL_INPUT:
			if (PORTC1 == INPUT_ON) {
				PORTC1 = INPUT_OFF;
			}
			if (PORTC2 == INPUT_OFF) {
				PORTC2 = INPUT_ON;
			}
			break;
	}
}

void close_data_input(int input) {
	switch(input) {
		case ANALOG_INPUT:
			PORTC1 == INPUT_ON;
			break;
		case DIGITAL_INPUT:
			PORTC2 == INPUT_OFF;
			break;
		default:
			PORTC1 == INPUT_OFF;
			PORTC2 == INPUT_OFF;
			break;
	}
}

void close_output() {
	PORTC0 == INPUT_OFF;
}
void open_output() {
	PORTC0 == INPUT_ON;
}
