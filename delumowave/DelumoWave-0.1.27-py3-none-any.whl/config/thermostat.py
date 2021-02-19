STATE = {True: 0x55,
         False: 0xFF}

TARGET_TEMPERATURE = dict(MIN=5,
                          MAX=55)

TEMPERATURE_SHIFT = 40

THERMOSTAT = dict()

THERMOSTAT[0xA4] = dict(PROCEDURE={'SWITCH_ON': 0x01,
                                   'STEP_UP': 0x01,
                                   'SWITCH_INVERSION': 0x02,
                                   'SWITCH_OFF': 0x04,
                                   'STEP_DOWN': 0x04,
                                   'GLOBAL_ON': 0x06,
                                   'GLOBAL_OFF': 0x07,
                                   'SET_MODE': 0x0A,
                                   'RESET_MODE': 0x0D,
                                   },
                        EEPROM={'ADDRESS_NUMBER': 8,
                                'ADDRESS_SIZE': 4,
                                'START_SENSORS_ADDRESS': 0xC0,

                                'FIRMWARE_VERSION': 0xE0,
                                'HARDWARE_TYPE': 0xE8,
                                'STATE': 0xED,
                                'OPERATION_MODE': 0xEE,
                                'TARGET_TEMPERATURE': 0xEF,
                                'CURRENT_TEMPERATURE': 0xF0,
                                }
                        )
