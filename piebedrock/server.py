from pieraknet.server import Server as RakNetServer
from piebedrock.interface import GameInterface

class BedrockServer:

    def main(self):
        interface = GameInterface()
        server = RakNetServer(logginglevel = "INFO")
        server.interface = interface

        server.start()

if __name__ == '__main__':
    server = BedrockServer()
    server.main()