from piebedrock.packets.packet import BedrockPacket


# Packet name: Login
# Packet ID: 0x01 (1)
# Bound to: Server
# Fields:
#
#  Protocol Version: Int (Big Endian).
#
#  Chain data: JSON array of JWT data.
#      Contains the display name, UUID and XUID.
#
#  Skin data: JWT data

class LoginPacket(BedrockPacket):
    PACKET_ID = 0x01
    PACKET_TYPE = "login"

    def __init__(self):
        super().__init__()
        self.protocol_version = None,
        self.chain_data = None,
        self.skin_data = None

    def decode_payload(self):
        self.protocol_version = self.read_int()
        self.chain_data = self.read_string()
        self.skin_data = self.read_string()
