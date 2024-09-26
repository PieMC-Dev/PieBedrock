from piebedrock.buffer import BedrockBuffer as Buffer
from piebedrock.packets.network_settings import NetworkSettingsPacket
from pieraknet.packets.frame_set import FrameSetPacket

class GameInterface:
    def __init__(self, server):
        self.server = server  # Aquí pasamos la referencia de BedrockServer

    def on_game_packet(self, frame, connection):
        # Verificar si el paquete tiene suficientes bytes
        if len(frame['body']) < 4:
            print("Packet too short.")
            return
        
        # Verificar si el tercer byte es del tipo de paquete de juego (0xc1)
        if frame['body'][2] == 0xc1:
            # Extraer los últimos 4 bytes
            protocol_version = frame['body'][-4:]
            buffer = Buffer(protocol_version)  # Crear un buffer con esos bytes
            version = buffer.read_int_be()  # Leer el primer byte como versión
            print(f"Minecraft Bedrock protocol version from {connection.address} is {version}")
            print(self.server.raknet.max_player_count)

            if version == self.server.raknet.game_protocol_version:
                print("Same Protocol")
                
                # Crear un paquete de configuración de red
                networkSettingPacket = NetworkSettingsPacket()
                networkSettingPacket.compression_threshold = 1
                networkSettingPacket.compression_method = 0
                networkSettingPacket.client_throttle_enabled = False
                networkSettingPacket.client_throttle_threshold = 0
                networkSettingPacket.client_throttle_scalar = 0.0
                networkSettingPacket.encode()  # Codificar el paquete

                packet_to_send = networkSettingPacket.getvalue() 

                self.create_frame_and_frame_set(connection, packet_to_send, flags=0x60)

            elif version > self.server.raknet.game_protocol_version:
                print(f"Client has a higher protocol version than the server. Please update the server.")
                return
            elif version < self.server.raknet.game_protocol_version:
                print(f"Client has a lower protocol version than the server. Please update the client.")
                return
            else:
                print("Unknown protocol version.")
                return
        else:
            print("Not a game packet.")

    def create_frame_and_frame_set(self, connection, body, flags=0x60):

        frame_set_packet = FrameSetPacket()
        frame_set_packet.create_frame(OnlinePongPacket, flags=0x64)

        # Codificar y enviar directamente sin usar Buffer
        connection.send_data(frame_set_packet.encode())
    
        # Longitud del cuerpo en bytes
        length_in_bytes = len(body).to_bytes(1, byteorder='big')

        # Añadir los bytes \xfe\x06 al inicio del cuerpo
        prefixed_body = b'\xfe' + length_in_bytes + body

        frame = RakNetFrame()
        frame.body = prefixed_body
        frame.flags = flags

        print(f"Frame Body: {prefixed_body}")

        # Crear un paquete de conjunto de tramas utilizando el frame
        frame_set_packet = RakNetFrameSetPacket()
        frame_set_packet.sequence_number = connection.client_sequence_number
        frame_set_packet.frames.append(frame)

        # Crear un buffer para empaquetar el frame set
        buffer = Buffer()
        frame_set_packet.encode(buffer)

        # Enviar el frame set
        connection.send_data(buffer.getvalue())
        print(f"FrameSet created and sent to {connection.address}")
