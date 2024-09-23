from piebedrock.packets.packet import BedrockPacket

class NetworkSettingsPacket(BedrockPacket):
    PACKET_ID = 0x8F
    PACKET_TYPE = "network_settings"

    def __init__(self, data: bytes = b''):
        super().__init__(data)
        self.compression_threshold = 0
        self.compression_method = 0
        self.client_throttle_enabled = False
        self.client_throttle_threshold = 0
        self.client_throttle_scalar = 0.0

    def encode_payload(self):
        self.write_short(self.compression_threshold)
        self.write_short(self.compression_method)
        self.write_bool(self.client_throttle_enabled)
        self.write_byte(self.client_throttle_threshold)
        self.write_float(self.client_throttle_scalar)