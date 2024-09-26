from pieraknet.server import Server as RakNetServer
from piebedrock.interface import GameInterface

class BedrockServer:
    def __init__(self):
        self.raknet = RakNetServer()
        self.interface = GameInterface(self)
        
        # Configurar el servidor RakNet
        self.raknet.logger.setLevel("INFO")
        self.raknet.game = "MCPE"
        self.raknet.name = "My Minecraft Server"
        self.raknet.modt = "PieBedrock Server"
        self.raknet.max_player_count = 10
        self.raknet.game_protocol_version = 712
        self.raknet.interface = self.interface
        
        # Configurar IP y puerto si es que son propiedades
        self.raknet.hostname = "0.0.0.0"  # Configuración de la IP
        self.raknet.port = 19132    # Configuración del puerto

    def start(self):
        print("Starting Bedrock Server...")
        self.raknet.start()

    def stop(self):
        print("Stopping Bedrock Server...")
        self.raknet.stop()

if __name__ == '__main__':
    server = BedrockServer()
    server.start()
