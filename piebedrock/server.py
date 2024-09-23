from pieraknet.server import Server as RakNetServer

class BedrockServer:
    def __init__(self):
        self.protocol_version = 712

    def main(self):
        from piebedrock.interface import GameInterface
        server = BedrockServer()
        interface = GameInterface()
        server = RakNetServer()
        server.logger.setLevel("INFO")
        server.game="MCPE"
        server.name="My Minecraft Server"
        server.modt="PieBedrock Server"
        server.interface = interface

        server.start()

if __name__ == '__main__':
    server = BedrockServer()
    server.main()