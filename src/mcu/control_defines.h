//#ifndef CONTROL_DEFINES_H
//#define CONTROL_DEFINES_H
/*
 * Definitions of constants for controls MCU-MCU communication.
 * General definition: TARGETDEVICE_COMMAND value (in hex)
 */

// Commands for USART from Main control Unit (MCU).
// 
#define USART_NOOP 0x0
#define WT32_RESET 0x1

// Commands from USART to MCU. 

// Datapath configuration, general values.
#define MCU_ANALOG_ON 0x2
#define MCU_DIGITAL_ON 0x1
#define MCU_OUTPUT_ON 0x4

#define MCU_OPCODE 0x3 
#define MCU_COMMAND 0xFC

#define OPC_INPUT 0x0
#define OPC_DATAP 0x3

// 
// bit mask for whether or not the chip is in data mode.
#define WT_DATA_MODE 0x20
//#endif
