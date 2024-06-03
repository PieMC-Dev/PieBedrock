from piebedrock.packets.packet import BedrockPacket


# Packet name: Disconnect
# Packet ID: 0x05
# Bound to: Client
# Fields:
#
#   Hide disconnect screen: Boolean.
#       Specifies if the disconnection screen should be
#       hidden when the client is disconnected, meaning
#       it will be sent directly to the main menu.
#
#   Kick message: String.
#       An optional message to show when disconnected.

class DisconnectPacket(BedrockPacket):
    PACKET_ID = 0x05
    PACKET_TYPE = "disconnect"

    def __init__(self, hide_disconnect_screen: bool = True, kick_message: str = ""):
        super().__init__()
        self.hide_disconnect_screen = hide_disconnect_screen
        self.kick_message = kick_message

    def encode_payload(self):
        self.write_bool(self.hide_disconnect_screen)
        self.write_string(self.kick_message)
