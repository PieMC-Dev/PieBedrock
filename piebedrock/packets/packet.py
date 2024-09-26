from piebedrock.buffer import BedrockBuffer


class BedrockPacket(BedrockBuffer):
    PACKET_ID: int = None
    PACKET_TYPE: str = None

    def encode_header(self):
        self.write_packet_id(self.PACKET_ID)
        self.write_byte(1)

    def decode_header(self):
        return self.read_packet_id()

    def encode(self):
        self.encode_header()
        if hasattr(self, 'encode_payload'):
            self.encode_payload()

    def decode(self):
        self.decode_header()
        if hasattr(self, 'decode_payload'):
            self.decode_payload()
