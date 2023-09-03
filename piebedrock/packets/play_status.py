from piebedrock.packets.packet import BedrockPacket

# Packet name: Play Status
# Packet ID: 0x02 (2)
# Bound to: Client
# Fields:
#
#   Status: Int (Big Endian).
#       The current status of the connection. [0]


# [0] Values for each status:
#
#   Login Success: 0.
#       Sent after Login has been successfully decoded
#       and the player has logged in.
#
#   Failed Client: 1.
#       Displays "Could not connect: Outdated client!".
#
#   Failed Server: 2.
#       Displays "Could not connect: Outdated server!".
#
#   Player Spawn: 3.
#       Sent after world data to spawn the player.
#
#   Failed Invalid Tenant: 4.
#       Displays "Unable to connect to world.
#       Your school does not have access to this server."
#
#   Failed Vanilla Edu: 5.
#       Displays "The server is not running
#       Minecraft: Education Edition. Failed to connect."
#
#   Failed Incompatible: 6.
#       Displays "The server is running an incompatible
#       edition of Minecraft. Failed to connect."
#
#   Failed Server Full: 7.
#       Displays "Wow this server is popular! Check back
#       later to see if space opens up. Server Full"

class PlayStatusPacket(BedrockPacket):
    packet_id = 0x02
    packet_type = "play_status"

    status: int = None

    def encode_payload(self):
        self.write_int_be(self.status)
