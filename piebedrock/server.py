import threading
from pieraknet.server import Server as PieRakNet
from pieraknet.packets.game_packet import GamePacket
from pieraknet.connection import Connection as RakNetConnection
from pieraknet.packets.frame_set import Frame

import logging
import os
import time
import random

class BedrockServer:
    def __init__(self, hostname="0.0.0.0", port=19132, logger=None, gamemode="survival", timeout=20, logginglevel="DEBUG", dev_mode=False):
        if logger is None:
            logger = logging.getLogger("PieBedrock")
            logger.setLevel(getattr(logging, logginglevel.upper()))
            formatter = logging.Formatter('%(asctime)s [%(name)s - %(levelname)s] - %(message)s', "%H:%M:%S")
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self.initialized = False
        self.logger = logger
        self.server_status = None
        self.hostname = hostname
        self.port = port
        self.edition = "MCPE"
        self.protocol_version = 594
        self.version_name = "1.20.12"
        self.name = "PieBedrock Server"
        self.motd = "GitHub/@PieMC-Dev"
        self.players_online = 0
        self.max_players = 20
        self.gamemode_map = {
        "survival": 1,
        "creative": 2,
        "adventure": 3
        }
        self.gamemode = gamemode.lower().capitalize()
        self.gamemodeId = self.gamemode_map.get(self.gamemode.lower(), None)
        self.port_v6 = 19131
        self.guid = random.randint(1, 99999999)
        self.uid = random.randint(1, 99999999)
        self.raknet_version = 11
        self.timeout = timeout
        self.running = False
        self.start_time = int(time.time())
        self.pieraknet_thread = None
        self.dev_mode = dev_mode

    def pieraknet_init(self):
        self.update_server_status()
        self.pieraknet = PieRakNet(self.hostname, self.port, responseData=self.server_status)
        self.pieraknet.timeout = self.timeout
        self.initialized = True

    def get_time_ms(self):
        return round(time.time() - self.start_time, 3)

    def update_server_status(self):
        self.server_status = ";".join([
            self.edition,
            self.name,
            f"{self.protocol_version}",
            self.version_name,
            f"{self.players_online}",
            f"{self.max_players}",
            f"{self.uid}",
            self.motd,
            self.gamemode.lower().capitalize(),
            f"{self.gamemodeId}",
            f"{self.port}",
            f"{self.port_v6}"
        ]) + ";"
        self.server_status

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
            self.pieraknet_init()
        self.running = True
        self.logger.info(f"Running on {self.hostname}:{str(self.port)} ({str(self.get_time_ms())}s).")
        self.pieraknet.start()

    def stop(self):
        self.logger.info("Stopping...")
        self.running = False
        if self.pieraknet_thread:
            self.pieraknet.stop()
            self.pieraknet_thread.join()
        self.logger.info("Stop")
