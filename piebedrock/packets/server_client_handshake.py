from piebedrock.packets.packet import BedrockPacket

# TODO Packet documentation

class ServerClientHandshakePacket(BedrockPacket):
    PACKET_ID = 0x03
    PACKET_TYPE = "server_client_handshake"

    jwt_data: str = None

    def encode_payload(self): # TODO
        self.write_string(self.jwt_data)
