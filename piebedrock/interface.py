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
                networkSettingPacket.compression_threshold = 0
                networkSettingPacket.compression_method = 0
                networkSettingPacket.client_throttle_enabled = False
                networkSettingPacket.client_throttle_threshold = 0
                networkSettingPacket.client_throttle_scalar = 0.0
                networkSettingPacket.encode()  # Codificar el paquete
                frame['body'] = networkSettingPacket.getvalue()

                self.create_frame_and_frame_set(connection, frame['body'], flags=0x64)

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

        # Longitud del cuerpo en bytes
        length_in_bytes = len(body).to_bytes(1, byteorder='big')

        # Añadir los bytes \xfe\x06 al inicio del cuerpo
        prefixed_body = b'\xfe' + length_in_bytes + body

        # Crear el FrameSetPacket y asignar el número de secuencia
        frame_set_packet = FrameSetPacket(self.server.raknet)
        frame_set_packet.create_frame(prefixed_body, flags)

        # Establecer el número de secuencia del servidor
        frame_set_packet.set_sequence_number(connection.server_sequence_number)

        print(f"Frame Body: {prefixed_body}")
        
        # Codificar y enviar directamente sin usar Buffer
        connection.send_data(frame_set_packet.encode())

        print(f"FrameSet created and sent to {connection.address}")
