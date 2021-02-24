"""Enables interaction with the linear controller.
"""
from enum import Enum


class LinearControllerMessage(Enum):
    SETUP_FINISHED = 100
    RESET_FINISHED = 101
    SET_BATCH_SIZE_FINISHED = 102
    SET_EXPOSURE_US_FINISHED = 103
    # SET_INPUT_TIME_FINISHED = 104  # Historically for use of input time controller-side
    SET_LOW_VALUE_FINISHED = 105
    START_WITH_LOW_VALUE_FINISHED = 106
    START_WITH_HIGH_VALUE_FINISHED = 107
    MAX_BATCH_SIZE_ERROR = 108


class LinearController:
    def __init__(self, batch_size: int = 1024, exposure_us: int = 24, low_value: float = 2.2,
                 start_with_low: bool = True, port: str = '/dev/ttyACM0', verbose_level: int = 0):
        self.initialized = False  # While we are not initialized, we don't run the resets (reset only once after init)
        self.port = port
        self.serial_connection = None
        # TODO: verbosity should be hooked-up in lightonopu system.
        self.verbose_level = verbose_level  # 0: no messages, 1: some messages, 2: all/debug messages

        # Set-up basic parameters:
        self.__exposure_us, self.__batch_size, self.__start_with_low, self.__low_value = None, None, None, None
        # store init params for later at open because can not send signal before serial connection is open
        self.parameters = {"batch_size": batch_size,
                           "exposure_us": exposure_us,
                           "start_with_low": start_with_low,
                           "low_value": low_value}

        if self.verbose_level >= 1:
            print("Linear controller initialized.")

    @property
    def exposure_us(self):
        return self.__exposure_us

    @exposure_us.setter
    def exposure_us(self, target_value):
        if target_value != self.exposure_us:
            # Serial command to set exposure is of the form 'e{EXPOSURE_VALUE}':
            command = 'e' + str(target_value)  # TODO: command and finished messages should be paired in a nicer way.
            self._send_serial_command(command, LinearControllerMessage.SET_EXPOSURE_US_FINISHED)
            self.__exposure_us = target_value
            if self.verbose_level >= 2:
                print(f"Linear controller: new exposure set to {self.exposure_us}.")

    @property
    def batch_size(self):
        return self.__batch_size

    @batch_size.setter
    def batch_size(self, target_value):
        if target_value != self.batch_size:
            # Serial command to set batch size is of the form 'b{BATCH_SIZE}':
            command = 'd' + str(target_value)
            self._send_serial_command(command, LinearControllerMessage.SET_BATCH_SIZE_FINISHED)
            self.__batch_size = target_value
            self.reset()
            if self.verbose_level >= 2:
                print(f"Linear controller: new batch size set to {self.batch_size}.")

    @property
    def low_value(self):
        return self.__low_value

    @low_value.setter
    def low_value(self, target_value):
        if target_value < 0 or target_value > 10:
            raise ValueError(f"New low value {target_value} is out of range (0-10).")
        else:
            command = 'v' + str(target_value)
            self._send_serial_command(command, LinearControllerMessage.SET_LOW_VALUE_FINISHED)
            self.__low_value = target_value
            self.reset()
            if self.verbose_level >= 2:
                print(f"Linear controller: new low value set to {self.low_value}.")

    @property
    def start_with_low(self):
        return self.__start_with_low

    @start_with_low.setter
    def start_with_low(self, target_value):
        if target_value != self.start_with_low:
            if target_value:  # Start with low
                command = 'low_voltage'  # TODO: obfuscate.
                self._send_serial_command(command, LinearControllerMessage.START_WITH_LOW_VALUE_FINISHED)
            else:
                command = 'high_voltage'  # TODO: obfuscate.
                self._send_serial_command(command, LinearControllerMessage.START_WITH_HIGH_VALUE_FINISHED)
            self.__start_with_low = target_value
            self.reset()
            if self.verbose_level >= 2:
                if target_value:
                    print(f"Linear controller: now starting with low value first (fast transition first).")
                else:
                    print(f"Linear controller: now starting with high value first (slow transition first).")

    def _send_serial_command(self, command, finished_message: LinearControllerMessage):
        """Execute a serial command and wait for its execution before returning."""
        self.serial_connection.write(str.encode(command))
        self._wait_for_serial_completion(finished_message)
        # TODO: offer a way to do this asynchronously (thread + .is_ready() status check).

    def _wait_for_serial_completion(self, finished_message: LinearControllerMessage):
        """Wait for a completion message on the serial channel and return."""
        answer = self.serial_connection.read(1)
        if not answer:
            raise TimeoutError(f"Controller timeout")
        if ord(answer) == LinearControllerMessage.MAX_BATCH_SIZE_ERROR.value:
            raise RuntimeError(f"Maximum batch size value is 2,147,483,647: please use a correct value.")
        elif ord(answer) != finished_message.value:
            raise RuntimeError(f"Got unexpected controller message")

    def __enter__(self):
        self.open()

    def __exit__(self, *args):
        self.close()

    def open(self, exposure_us=None, batch_size=None):
        # Import here to avoid module import errors when drivers dependencies aren't installed
        # noinspection PyUnresolvedReferences
        import serial
        # Set-up the connection with the linear controller
        self.serial_connection = serial.Serial(self.port, baudrate=115200, timeout=10)
        self._wait_for_serial_completion(LinearControllerMessage.SETUP_FINISHED)
        # set parameters to values at init
        for key in self.parameters:
            setattr(self, key, self.parameters[key])
        # set initialized and reset the batch counter
        self.initialized = True
        self.reset()
        if batch_size is not None:
            self.batch_size = batch_size
        if exposure_us is not None:
            self.exposure_us = exposure_us
        if self.verbose_level >= 2:
            print("Linear controller: serial connection opened.")

    def close(self):
        if self.serial_connection is None:
            print("No serial connection to close")
        else:
            # we reset these values to None so that at next open a message
            # is sent to the controller. If we do not do this, the controller
            # uses its own default values.
            self.__exposure_us, self.__batch_size, self.__start_with_low, self.__low_value = None, None, None, None
            self.serial_connection.close()

    def reset(self):
        # Serial command for reset is simply 'reset':
        if self.initialized:
            self._send_serial_command('reset', LinearControllerMessage.RESET_FINISHED)
            if self.verbose_level >= 2:
                print(f"Linear controller: status reset, batch counter set to zero.")

    def __getstate__(self):
        """Closes and return current state"""
        state = {"initialized": self.initialized,
                 "serial_connection": self.serial_connection,
                 "batch_size": self.batch_size,
                 "exposure_us": self.exposure_us,
                 "low_value": self.low_value,
                 "start_with_low": self.start_with_low,
                 "port": self.port,
                 "verbose_level": self.verbose_level
                 }
        self.close()
        return state

    def __setstate__(self, state):
        """Restore object with given state"""
        self.__init__(state["batch_size"], state["exposure_us"], state["low_value"],
                      state["start_with_low"], state["port"], state["verbose_level"])
        # If state was active then open controller
        if state["initialized"]:
            self.open(exposure_us=state["exposure_us"], batch_size=state["batch_size"])
