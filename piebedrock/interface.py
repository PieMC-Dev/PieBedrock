from piebedrock.buffer import BedrockBuffer as Buffer

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
            print(f"Protocol version in hex: {protocol_version}")
            print(f"Minecraft Bedrock protocol version: {version}")
        else:
            print("Not a game packet.")
