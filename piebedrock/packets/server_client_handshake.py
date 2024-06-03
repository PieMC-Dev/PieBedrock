from piebedrock.packets.packet import BedrockPacket


# TODO Packet documentation

class ServerClientHandshakePacket(BedrockPacket):
    PACKET_ID = 0x03
    PACKET_TYPE = "server_client_handshake"

    def __init__(self, jwt_data: Union[str, None] = None):
        super().__init__()
        self.jwt_data = jwt_data

    def encode_payload(self):
        self.write_string(self.jwt_data)
