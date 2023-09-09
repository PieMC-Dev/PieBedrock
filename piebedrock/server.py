from pieraknet import Server as RakNetServer
from pieraknet.packets.game_packet import GamePacket
from pieraknet.connection import Connection as RakNetConnection
from pieraknet.packets.frame_set import Frame

import logging
import os
import time
import random

class BedrockServer:
    def __init__(self, hostname="0.0.0.0", port=19132, logger=logging.getLogger("PieBedrock"), gamemode="survival", timeout=20):
        self.initialized = False
        self.logger = logger
        self.server_status = None
        self.hostname = hostname
        self.port = port
        self.edition = "MCPE"
        self.protocol_version = 594
        self.version_name = "1.20.12"
        self.motd1 = "PieBedrock Server"
        self.motd2 = "GitHub/@PieMC-Dev"
        self.players_online = 0
        self.max_players = 20
        self.gamemode_map = {
            "survival": ("Survival", 1),
            "creative": ("Creative", 2),
            "adventure": ("Adventure", 3)
        }
        self.gamemode = self.gamemode_map.get(gamemode, ("Survival", 0))
        self.port_v6 = 19131
        self.guid = random.randint(1, 99999999)
        self.uid = random.randint(1, 99999999)
        self.raknet_version = 11
        self.timeout = timeout
        self.running = False
        self.start_time = int(time.time())

    def raknet_init(self):
        self.raknet_server = RakNetServer(self.hostname, self.port, logging.getLogger("PieRakNet"))
        self.raknet_server.interface = self
        self.update_server_status()
        self.raknet_server.protocol_version = self.raknet_version
        self.raknet_server.timeout = self.timeout
        self.initialized = True
        
    def get_time_ms(self):
        return round(time.time() - self.start_time, 3)

    def update_server_status(self):
        self.server_status = ";".join([
            self.edition,
            self.motd1,
            f"{self.protocol_version}",
            self.version_name,
            f"{self.players_online}",
            f"{self.max_players}",
            f"{self.uid}",
            self.motd2,
            self.gamemode[0],
            f"{self.gamemode[1]}",
            f"{self.port}",
            f"{self.port_v6}"
        ]) + ";"
        self.raknet_server.name = self.server_status

    def on_game_packet(self, packet: GamePacket, connection: RakNetConnection):
        packet.decode()
        if packet.body[0] == 0x01:
            self.logger.info(f"New Login Packet: {str(packet.body)}")

    def on_new_incoming_connection(self, connection: RakNetConnection):
        self.logger.info(f"New Incoming Connection: {str(connection.address)}")

    def on_disconnect(self, connection: RakNetConnection):
        self.logger.info(f"{str(connection.address)} disconnected")

    def on_unknown_packet(self, packet: Frame, connection: RakNetConnection):
        self.logger.info(f"New Unknown Packet: {str(packet.body)}")

    def start(self):
        if not self.initialized:
            self.raknet_init()
        self.running = True
        self.raknet_thread.start()
        self.logger.info(f"Running on {self.hostname}:{str(self.port)} ({str(self.get_time_ms())}s).")
            
    def stop(self):
        self.logger.info("Stopping...")
        self.running = False
        self.raknet_server.stop()
        self.logger.info("Stop")
