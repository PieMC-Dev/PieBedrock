from piebedrock.packets.packet import BedrockPacket

# TODO Packet documentation

class ServerClientHandshakePacket(BedrockPacket):
    packet_id = 0x03
    packet_type = "server_client_handshake"

    jwt_data: str = None

    def encode_payload(self): # TODO
        self.write_string(self.jwt_data)
