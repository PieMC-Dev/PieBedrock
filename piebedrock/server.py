from pieraknet.server import Server as RakNetServer

class BedrockServer:
    #init
    def __init__(self):
        self.protocol_version = 712

    def main(self):
        from piebedrock.interface import GameInterface
        interface = GameInterface()
        server = RakNetServer(logginglevel = "INFO")
        server.interface = interface

        server.start()

if __name__ == '__main__':
    server = BedrockServer()
    server.main()