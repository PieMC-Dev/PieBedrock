from piebedrock.packets.packet import BedrockPacket
from typing import Union


# Packet name: Server Client Handshake
# Packet ID: 0x03 (3)
# Bound to: Client
# Fields:
#
#   JWT data: String.
#       The JWT data to send to the server.

class ServerClientHandshakePacket(BedrockPacket):
    PACKET_ID = 0x03
    PACKET_TYPE = "server_client_handshake"

    def __init__(self, jwt_data: Union[str, None] = None):
        super().__init__()
        self.jwt_data = jwt_data

    def encode_payload(self):
        self.write_string(self.jwt_data)
