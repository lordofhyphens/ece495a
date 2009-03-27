#ifndef CONTROL_DEFINES_H
#define CONTROL_DEFINES_H
/*
 * Definitions of constants for controls MCU-MCU communication.
 * General definition: TARGETDEVICE_COMMAND value
 */

// Commands for USART from Main control Unit (MCU).
// 
#define USART_NOOP 0x0
#define WT32_RESET 0x1

// Commands from USART to MCU. 

// Datapath configuration, general values.
#define ANALOG_ON 0x1
#define DIGITAL_ON 0x2
#define OUTPUT_ON 0x4
// Presets for the "known" states allowed (for the output ports).
#define MCU_A_ON_D_ON_O_ON 0x7
#define MCU_A_OFF_D_OFF_O_OFF 0x0
#define MCU_A_OFF_D_ON_O_OFF 0x2
#define MCU_A_OFF_D_ON_O_ON 0x6
#define MCU_A_ON_D_OFF_O_OFF 0x1
#define MCU_A_ON_D_OFF_O_ON  0x5

#endif
