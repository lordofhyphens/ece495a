/** Function prototypes for main control logic.
**/

// On/off constants.
#define INPUT_ON = 1;
#define INPUT_OFF = 0;

// Some defines to enumerate the input ports we'll be using
#define ANALOG_INPUT = 0;
#define DIGITAL_INPUT = 1;

void reset_UART();

// Configures the datapath for a given setup. Only one "port" can be open at once.
void open_data_input(int input);
void close_data_input(int input);

void mcu_pin_init();
unsigned char decode_datapath_code(char command, char port);
unsigned char send_usart_command(unsigned char);
