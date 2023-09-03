import struct
import uuid
from pieraknet.buffer import Buffer

# TODO NBT
# TODO ByteArray
# TODO BlockCoordinates
# TODO PlayerLocation

# Info about data types can be found here:
# https://wiki.vg/Bedrock_Protocol

class BedrockBuffer(Buffer):
    def read_int_be(self):
        data = self.read(4)
        return struct.unpack('>i', data)[0]

    def write_int_be(self, data):
        packed_data = struct.pack('>i', data)
        self.write(packed_data)

    def read_int(self):
        data = self.read(4)
        return struct.unpack('<i', data)[0]

    def write_int(self, data):
        packed_data = struct.pack('<i', data)
        self.write(packed_data)

    def read_unsigned_int(self):
        data = self.read(4)
        return struct.unpack('<I', data)[0]

    def write_unsigned_int(self, data):
        packed_data = struct.pack('<I', data)
        self.write(packed_data)

    def read_string(self):
        length = self.read_unsigned_var_int()
        data = self.read(length)
        return data.decode('utf-8')

    def write_string(self, data):
        encoded_data = data.encode('utf-8')
        length = len(encoded_data)
        self.write_unsigned_var_int(length)
        self.write(encoded_data)

    def read_float(self):
        data = self.read(4)
        return struct.unpack('<f', data)[0]

    def write_float(self, data):
        packed_data = struct.pack('<f', data)
        self.write(packed_data)

    def read_var_int(self):
        value = 0
        shift = 0
        while True:
            byte = self.read(1)[0]
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return value

    def write_var_int(self, data):
        while True:
            byte = data & 0x7F
            data >>= 7
            if data:
                byte |= 0x80
            self.write(bytes([byte]))
            if not data:
                break

    def read_signed_var_int(self):
        value = self.read_var_int()
        if value & 0x80000000:
            value -= 0x100000000
        return value

    def write_signed_var_int(self, data):
        if data < 0:
            data += 0x100000000
        self.write_var_int(data)

    def read_var_long(self):
        value = 0
        for i in range(10):
            b = self.read_byte()
            value |= (b & 0x7F) << (7 * i)
            if not (b & 0x80):
                break
        return value

    def write_var_long(self, data):
        for i in range(10):
            if data & ~0x7F == 0:
                self.write_byte(data)
                break
            else:
                self.write_byte((data & 0x7F) | 0x80)
                data >>= 7

    def read_signed_var_long(self):
        value = self.read_var_long()
        if value & 0x8000000000000000:
            value -= 0x10000000000000000
        return value

    def write_signed_var_long(self, data):
        if data < 0:
            data += 0x10000000000000000
        self.write_var_long(data)

    def read_vector3(self):
        x = self.read_float()
        y = self.read_float()
        z = self.read_float()
        return (x, y, z)

    def write_vector3(self, data):
        x, y, z = data
        self.write_float(x)
        self.write_float(y)
        self.write_float(z)

    def read_vector2(self):
        x = self.read_float()
        y = self.read_float()
        return (x, y)

    def write_vector2(self, data):
        x, y = data
        self.write_float(x)
        self.write_float(y)

    def read_bytearray(self, length):
        data = []
        for _ in range(length):
            byte = self.read_byte()
            data.append(byte)
        return data

    def write_bytearray(self, data):
        for byte in data:
            self.write_byte(byte)

    def read_uuid(self):
        data = self.read_bytearray(16)
        return uuid.UUID(bytes=data)

    def write_uuid(self, data):
        data_bytes = data.bytes if isinstance(data, uuid.UUID) else uuid.UUID(data).bytes
        self.write_bytearray(data_bytes)
