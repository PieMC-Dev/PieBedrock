from piebedrock.packets.packet import BedrockPacket

# Packet name: Resource Packs Info
# Packet ID: 0x06 (6)
# Bound to: Client
# Fields:
#
#   Forced to accept: Boolean.
#       If the resource pack requires the client accept it.
#
#   Scripting enabled: Boolean.
#       If scripting is enabled.
#
#   BehaviorPackInfos: ResourcePackInfo[].
#       A list of behaviour packs that the client needs
#       to download before joining the server. All of these
#       behaviour packs will be applied together.
#
#   ResourcePackInfos: ResourcePackInfo[].
#       A list of resource packs that the client needs
#       to download before joining the server. The order
#       of these resource packs is not relevant in this
#       packet. It is however important in the Resource Pack
#       Stack packet.

# TODO Packet class
