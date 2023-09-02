from bedrockproto.packets.packet import BedrockPacket

class LoginPacket(BedrockPacket):
    packet_id = 0x01
    packet_type = "login"

    def decode_payload(self):
        pass
