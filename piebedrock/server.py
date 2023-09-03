from pieraknet import Server as RakNetServer
from pieraknet.packets.game_packet import GamePacket
from pieraknet.connection import Connection as RakNetConnection
import logging
import os
import time
import random

class BedrockServer:
    
    def __init__(self, hostname="0.0.0.0", port=19132, logger=logging.getLogger("PieBedrock")):
        self.logger = logger
        self.hostname = hostname
        self.port = port
        self.port_v6 = 19131
        self.logger.debug("Initializing...")
        self.server_status = None
        self.edition = "MCPE"
        self.protocol_version = 594
        self.version_name = "1.20.12"
        self.motd1 = "PieBedrock"
        self.motd2 = "Server"
        self.players_online = 0
        self.max_players = 20
        self.players = []
        self._gamemode_map = {
            "survival": ("Survival", 1),
            "creative": ("Creative", 2),
            "adventure": ("Adventure", 3)
        }
        try:
            self.set_gamemode("survival")
        except KeyError:
            self.gamemode = ("Survival", 1)
        self.guid = random.randint(1, 99999999)
        self.uid = self.guid = random.randint(1, 99999999)
        self.timeout = 20
        self.raknet_version = 11
        self.raknet_server = RakNetServer(self.hostname, self.port, logging.getLogger('PieRakNet'))
        self.raknet_server.interface = self
        self.update_server_status()
        self.raknet_server.protocol_version = self.raknet_version
        self.raknet_server.timeout = self.timeout
        self.running = False
        self.start_time = int(time.time())

    def set_gamemode(self, gamemode):
        gm = gamemode.lower()
        if (gm in self._gamemode_map.keys()):
            self.gamemode = self._gamemode_map[gm]
        else:
            raise KeyError(f"Gamemode {str(gamemode)} not exists")

    def update_server_status(self):
        self.server_status = ";".join([
            self.edition,
            self.motd1,
            str(self.protocol_version),
            self.version_name,
            str(self.players_online),
            str(self.max_players),
            str(self.uid),
            self.motd2,
            self.gamemode[0],
            str(self.gamemode[1]),
            str(self.port),
            str(self.port_v6),
        ])

    def on_new_incoming_connection(self, connection: RakNetConnection):
        self.logger.info(f"New Incoming Connection: {str(connection.address)}")

    def on_disconnect(self, connection: RakNetConnection):
        self.logger.info(f"Disconnected: {str(connection.address)}")

    def start(self):
        self.running = True
        self.raknet_server.start()

if __name__ == "__main__":
    server = BedrockServer()
    server.start()
