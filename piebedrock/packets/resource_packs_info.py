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

class ResourcePacksInfoPacket(BedrockPacket):
    PACKET_ID = 0x06

    def __init__(self):
        super().__init__()
        self.forced_to_accept = False
        self.scripting_enabled = False
        self.behavior_pack_infos = []
        self.resource_pack_infos = []

    def decode_payload(self, payload):
        self.forced_to_accept = payload.read_bool()
        self.scripting_enabled = payload.read_bool()
        
        behavior_pack_count = payload.read_var_int()
        self.behavior_pack_infos = [self.decode_pack_info(payload) for _ in range(behavior_pack_count)]

        resource_pack_count = payload.read_var_int()
        self.resource_pack_infos = [self.decode_pack_info(payload) for _ in range(resource_pack_count)]

    def encode_payload(self):
        payload = self.new_payload()
        payload.write_bool(self.forced_to_accept)
        payload.write_bool(self.scripting_enabled)

        payload.write_var_int(len(self.behavior_pack_infos))
        for pack_info in self.behavior_pack_infos:
            self.encode_pack_info(payload, pack_info)

        payload.write_var_int(len(self.resource_pack_infos))
        for pack_info in self.resource_pack_infos:
            self.encode_pack_info(payload, pack_info)

        return payload

    def decode_pack_info(self, payload):
        # Assuming ResourcePackInfo has fields like uuid, version, etc.
        pack_info = {
            'uuid': payload.read_string(),
            'version': payload.read_string(),
            'size': payload.read_unsigned_long(),
            # Add more fields as necessary
        }
        return pack_info

    def encode_pack_info(self, payload, pack_info):
        payload.write_string(pack_info['uuid'])
        payload.write_string(pack_info['version'])
        payload.write_unsigned_long(pack_info['size'])
        # Add more fields as necessary
