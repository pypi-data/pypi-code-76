import json
import logging
from threading import Thread

import kamzik3
from kamzik3 import CommandFormatException, DeviceServerError, DeviceError
from kamzik3.constants import *
from kamzik3.snippets.snippetDataAccess import rgetattr
from kamzik3.snippets.snippetsJson import JsonKamzikHook, JsonKamzikEncoder
from kamzik3.snippets.snippetsZmq import Worker


class DeviceWorker(Worker, Thread):

    def __init__(self, id, master_host, master_port, zmq_context=None):
        self.logger = logging.getLogger(u"Console.DeviceWorker@{}".format(id))
        Thread.__init__(self)
        Worker.__init__(self, id, master_host, master_port, zmq_context)
        self.instructions_set += [INSTRUCTION_COMMAND, INSTRUCTION_GET, INSTRUCTION_SET, INSTRUCTION_METHOD,
                                  INSTRUCTION_POLL, INSTRUCTION_INIT]

    def get_payload(self, data):
        try:
            instruction, device_id = data[0], data[1].decode()
            device = kamzik3.session.get_device(device_id)

            # Execute command directly on devices
            if instruction == INSTRUCTION_COMMAND:
                command, with_token = data[2].decode(), int(data[3])
                token = device.command(command, with_token=int(with_token))
                status, response = RESPONSE_OK, str(len(data[3]))

            # Get devices attribute
            elif instruction == INSTRUCTION_GET:
                attribute = json.loads(data[2].decode(), object_hook=JsonKamzikHook)
                response = device._get(attribute)
                response = json.dumps(response, cls=JsonKamzikEncoder, ensure_ascii=True)
                status, token = RESPONSE_OK, 0

            # Set devices attribute
            elif instruction == INSTRUCTION_SET:
                attribute, attribute_value = json.loads(data[2].decode(), object_hook=JsonKamzikHook)
                set_token = device.set_attribute(attribute, attribute_value)
                status, token, response = RESPONSE_OK, set_token, str(len(data[2]))

            # Execute devices method with attributes
            elif instruction == INSTRUCTION_METHOD:
                method, attributes = data[2].decode(), json.loads(data[3].decode(), object_hook=JsonKamzikHook)
                response = rgetattr(device, method)(**attributes)
                response = json.dumps(response, cls=JsonKamzikEncoder, ensure_ascii=True)
                status, token = RESPONSE_OK, 0

            # Poll devices for activity
            elif instruction == INSTRUCTION_POLL:
                status, token, response = RESPONSE_OK, 0, "1"

            # Init devices
            elif instruction == INSTRUCTION_INIT:
                if device is None:
                    raise DeviceServerError(
                        "Device {} is not registered on the server or publisher is not ready".format(device_id))
                elif not device.in_statuses(READY_DEVICE_STATUSES):
                    raise DeviceServerError("Device is not ready")
                else:
                    response = json.dumps(
                        (device.attributes, device.attributes_sharing_map,
                         device.exposed_methods, device.qualified_name), cls=JsonKamzikEncoder,
                        ensure_ascii=True)
                    status, token = RESPONSE_OK, 0
            # None of above, request not implemented
            else:
                status, token, response = RESPONSE_ERROR, 0, str(len(data[3]))

        except CommandFormatException as e:
            status, token, response = RESPONSE_ERROR, 0, "Command format error"
            self.logger.error("Command format error {} {}".format(str(data), e))
        except DeviceServerError as e:
            status, token, response = RESPONSE_ERROR, 0, "Device server error"
            self.logger.error("Device server error {} {}".format(str(data), e))
        except DeviceError as e:
            status, token, response = RESPONSE_ERROR, 0, "Command error: {}".format(e)
            self.logger.error("Command error {} {}".format(str(data), e))
        except (AttributeError, KeyError) as e:
            status, token, response = RESPONSE_ERROR, 0, "Attribute error: {}".format(e)
            self.logger.error("Attribute error {} {}".format(str(data), e))
        except Exception as e:
            status, token, response = RESPONSE_ERROR, 0, "Unknown error: {}".format(e)
            self.logger.error("Unknown error {} {}".format(str(data), e))
        finally:
            return [status.encode(), str(token).encode(), MSG_JSON, response.encode()]
