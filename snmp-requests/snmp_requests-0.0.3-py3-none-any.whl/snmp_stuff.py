#from scapy.all import *

class ASN1_object(object):

    # Class migth be:
    # UNIVERSAL (0)
    # APPLICATION (1)
    # PRIVATE (2)
    # CONTEXT-SPECIFIC (3)
    #class_number = 0

    # Build-in types mighth by:
    # Simple (0)
    # Constructed (1)
    #kind_of_type = 0

    # Universal types are:
    # Reserved for BER (0)
    # BOOLEAN (1)
    # INTEGER (2)
    # BIT STRING (3)
    # OCTET STRING (4)
    # NULL (5)
    # OBJECT IDENTIFIER (6)
    # ObjectDescriptor (7)
    # INTANCE OF, EXTERNAL (8)
    # REAL (9)

    # ENUMERATED (10)
    # EMBEDDED PDV (11)
    # UTF8String (12)
    # RELATIVE-OID (13)
    # SEQUENCE, SEQUENCE OF (16)
    # SET, SET OF (17)
    # NumericString (18)
    # PrintableString (19)
    #type = 0

    # Represent the length in octets of the value
    #length = 0

    # The value it self if a simple type or other ASN.1 objects when constructed
    #value = 0

    def __init__(self, class_number, kind_of_type, type, length, value):
        self.class_number = class_number
        self.kind_of_type = kind_of_type
        self.type = type
        self.tag = (self.class_number * 64) + (self.kind_of_type * 32) + self.type
        self.length = length
        self.value = value


    def encode_value(self):

        encoded = self.value
        return encoded


    def get_ber(self):

        encoding = []
        encoding.append(self.tag)
        encoding.append(self.length)
        encoding = encoding + self.encode_value()

        #if (self.kind_of_type == 0):
        #   encoding.append(self.value)
        #else:
        #    encoding = encoding + self.value.get_ber()

        return encoding




class INTEGER(ASN1_object):

    def __init__(self, value):
        class_number = 0   # Universal
        kind_of_type = 0   # Simple
        type = 2           # Integer

        # Calc length
        length = int(value / 255) + 1

        ASN1_object.__init__(self, class_number, kind_of_type, type, length, value)


    def encode_value(self):

        encoded = [self.value]
        return encoded



class OCTET_STRING(ASN1_object):

    def __init__(self, value):
        class_number = 0   # Universal
        kind_of_type = 0   # Simple
        type = 4           # OCTET STRING

        # Calc length
        length = len(value)

        ASN1_object.__init__(self, class_number, kind_of_type, type, length, value)


    def encode_value(self):

        encoded = []
        for c in self.value:
            encoded.append(ord(c))
        return encoded


class OBJECT_IDENTIFIER(ASN1_object):

    def __init__(self, value):
        class_number = 0   # Universal
        kind_of_type = 0   # Simple
        type = 6           # OBJECT IDENTIFIER

        # Calc length
        length = len(value.split('.'))-1

        ASN1_object.__init__(self, class_number, kind_of_type, type, length, value)


    def encode_value(self):

        encoded = self.value.split('.')
        return encoded



class VarBind(ASN1_object):

    def __init__(self, name, value):
        self.name = name
        self.val = value

        class_number = 0   # Universal
        kind_of_type = 1   # Constructed
        type = 16          # OBJECT IDENTIFIER

        # Calc length
        length = len(name.get_ber()) + len(value.get_ber())

        value = name.get_ber() + value.get_ber()

        ASN1_object.__init__(self, class_number, kind_of_type, type, length, value)


class VarBindList(ASN1_object):

    def __init__(self, varBinds):
        self.varBinds = varBinds

        class_number = 0   # Universal
        kind_of_type = 1   # Constructed
        type = 16          # OBJECT IDENTIFIER

        # Calc length
        length = 0
        for varBind in varBinds:
            length = length + len(varBind.get_ber())

        value = []
        for varBind in varBinds:
            value = value + varBind.get_ber()

        ASN1_object.__init__(self, class_number, kind_of_type, type, length, value)


class PDU(ASN1_object):

    def __init__(self, pdu_type, request_id, error_status, error_index, variable_bindings):
        self.pdu_type = pdu_type
        self.request_id = request_id
        self.error_status = error_status
        self.error_index = error_index
        self.variable_bindings = variable_bindings


        class_number = 0   # Universal
        kind_of_type = 1   # Constructed
        type = 16          # OBJECT IDENTIFIER

        # Calc length
        length = len(request_id.get_ber()) + len(error_status.get_ber()) + len(error_index.get_ber()) + len(variable_bindings.get_ber())

        value = request_id.get_ber() + error_status.get_ber() + error_index.get_ber() + variable_bindings.get_ber()




        ASN1_object.__init__(self, class_number, kind_of_type, type, length, value)


class GetRequest(PDU):

    def __init__(self, request_id, error_status, error_index, variable_bindings):

        pdu_type = 0    # GetRequest

        PDU.__init__(self, pdu_type, request_id, error_status, error_index, variable_bindings)



class Message(ASN1_object):

    def __init__(self, version, community, data):

        self.version = version
        self. community = community
        self.data = data

        class_number = 0  # Universal
        kind_of_type = 1  # Constructed
        type = 16  # OBJECT IDENTIFIER

        # Calc length
        length = len(version.get_ber()) + len(community.get_ber()) + len(data.get_ber())

        value = version.get_ber() + community.get_ber() + data.get_ber()


        ASN1_object.__init__(self, class_number, kind_of_type, type, length, value)


name = OBJECT_IDENTIFIER('1.3.6')
value = INTEGER(2)
varBind = VarBind(name, value)
varBindList = VarBindList([varBind])

payload = GetRequest(INTEGER(0), INTEGER(0), INTEGER(0), varBindList)
packet = Message(INTEGER(1), OCTET_STRING('public'), payload)

print(packet.get_ber())