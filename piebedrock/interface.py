from piebedrock.buffer import BedrockBuffer as Buffer
from piebedrock.server import BedrockServer
from pieraknet.connection import Connection as RakNetConnection
from pieraknet.server import Server as RaknetServer
from pieraknet.packets.frame_set import FrameSetPacket as RakNetFrameSetPacket
from pieraknet.packets.frame import Frame as RakNetFrame
from piebedrock.packets.network_settings import NetworkSettingsPacket

class GameInterface:
    def on_game_packet(self, packet_body, connection):
        # Check that the packet has enough bytes
        if len(packet_body) < 4:
            print("Packet too short.")
            return
        
        # Check if the third byte is the game packet type (0xc1)
        if packet_body[2] == 0xc1:
            # Extract the last 4 bytes
            protocol_version = packet_body[-4:]
            # Create a buffer with the last 4 bytes
            buffer = Buffer(protocol_version)
            # Read the first byte as version
            version = buffer.read_int_be()
            #print(f"Protocol version in hex: {protocol_version}")
            print(f"Minecraft Bedrock protocol version from {connection.address} is {version}")
            if version == BedrockServer().protocol_version:
                print(f"Same Protocol")
                networkSettingPacket = NetworkSettingsPacket()
                networkSettingPacket.compression_threshold = 0
                networkSettingPacket.compression_method = 0
                networkSettingPacket.client_throttle_enabled = False
                networkSettingPacket.client_throttle_threshold = 0
                networkSettingPacket.client_throttle_scalar = 0.0
                networkSettingPacket.encode()
                packetToSend = networkSettingPacket.getvalue()
                self.create_frame_and_frame_set(connection, packetToSend, flags=0x60)

            elif version > BedrockServer().protocol_version:
                print(f"Client has a higher protocol version than the server. Please update the server.")
                return
            elif version < BedrockServer().protocol_version:
                print(f"Client has a lower protocol version than the server. Please update the client.")
                return
            else:
                print(f"Unknown protocol version.")
                return
            
            #GameInterface().create_frame_and_frame_set(connection, packet_body, flags=0x00)
        else:
            print("Not a game packet.")

    def create_frame_and_frame_set(self, connection, body, flags=0x60):
        # Get the length of the body in bytes
        length_in_bytes = len(body).to_bytes(1, byteorder='big')  # Length as byte

        # Add the bytes \xfe\x06 at the start of the body
        # Example: fe 06 c1 01 00 00 02 c8
        # fe = RakNet game packet prefix
        # 06 = length of the Minecraft Bedrock protocol body
        prefixed_body = b'\xfe' + length_in_bytes + body

        frame = RakNetFrame()
        frame.body = prefixed_body
        frame.flags = flags

        print(prefixed_body)

        # Create a frame set using the frame
        frame_set_packet = RakNetFrameSetPacket()
        frame_set_packet.frames.append(frame)

        # Pack the frame set into a buffer
        buffer = Buffer()
        frame_set_packet.encode(buffer)

        # Send the frame set
        connection.send_data(buffer.getvalue())
        print(f"FrameSet created and sent to {connection.address}")
