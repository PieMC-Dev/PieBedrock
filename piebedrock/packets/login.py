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
    packet_id = 0x01
    packet_type = "login"

    def decode_payload(self):
        print(self.getvalue()) # TODO
