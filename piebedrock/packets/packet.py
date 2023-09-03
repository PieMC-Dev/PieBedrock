from piebedrock.buffer import BedrockBuffer

class BedrockPacket(Buffer):
    packet_id: int = None
    packet_type: str = None

    def encode_header(self, data):
        self.write_byte(data)
    
    def decode_header(self):
        return self.read_byte()

    def encode(self):
        self.encode_header(self.packet_id)
        if hasattr(self, "encode_payload"):
            self.encode_payload()

    def decode(self):
        self.decode_header()
        if hasattr(self, "decode_payload"):
            self.decode_payload()
