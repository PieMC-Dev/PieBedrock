from pieraknet import Server as RakNetServer
from pieraknet.packets.game_packet import GamePacket
from pieraknet.connection import Connection as RakNetConnection
from piemc.handlers.logger import create_logger
from pieraknet.packets.frame_set import Frame as RakNetFrame
from piemc.meta.protocol_info import ProtocolInfo
from piemc.handlers.lang import LangHandler

import logging
import os
import time
import random
import os
import random
import threading
import time
import piemc.config

class BedrockServer:
    def __init__(self):
        self.threads = []
        self.lang = LangHandler.initialize_language()
        self.logger = create_logger('PieBedrock')
        self.server_status = None
        self.hostname = piemc.config.HOST
        self.edition = "MCPE"
        self.protocol_version = 594
        self.version_name = "1.20.12"
        self.motd = piemc.config.MOTD
        self.level = "Powered by PieMC"
        self.players_online = 2  # 2 players online XD. Update (By andiri): YES :sunglasses:
        self.max_players = piemc.config.MAX_PLAYERS
        self.gamemode_map = {
            "survival": ("Survival", 1),
            "creative": ("Creative", 2),
            "adventure": ("Adventure", 3)
        }
        self.gamemode = self.gamemode_map.get(piemc.config.GAMEMODE.lower(), ("Survival", 0))
        self.logger.info(self.lang['NOT_EXISTING_GAMEMODE']) if self.gamemode[1] == 0 else None
        self.port = piemc.config.BEDROCK_PORT
        self.port_v6 = 19133
        self.guid = random.randint(1, 99999999)
        with open('pieuid.dat', 'r') as f:
            pieuid = f.read().strip()
        self.uid = pieuid
        self.raknet_version = 11
        self.timeout = 20
        self.raknet_server = RakNetServer(self.hostname, self.port, create_logger('PieRakNet'))
        self.raknet_server.interface = self
        self.update_server_status()
        self.raknet_server.protocol_version = self.raknet_version
        self.raknet_server.timeout = self.timeout
        # self.raknet_server.magic = ''
        self.raknet_thread = threading.Thread(target=self.raknet_server.start)
        self.raknet_thread.daemon = True
        self.threads.append(self.raknet_thread)
        self.running = False
        self.logger.info(self.lang['SERVER_INITIALIZED'])
        self.start_time = int(time.time())
        self.start()
        
    def get_time_ms(self):
        return round(time.time() - self.start_time, 4)

    def update_server_status(self):
        self.server_status = ";".join([
            self.edition,
            self.motd,
            f"{self.protocol_version}",
            self.version_name,
            f"{self.players_online}",
            f"{self.max_players}",
            f"{self.uid}",
            self.level,
            self.gamemode[0],
            f"{self.gamemode[1]}",
            f"{self.port}",
            f"{self.port_v6}"
        ]) + ";"
        self.raknet_server.name = self.server_status

    def on_game_packet(self, packet: GamePacket, connection: RakNetConnection):
        packet.decode()
        if packet.body[0] == ProtocolInfo.LOGIN:
            self.logger.info(f"New Login Packet: {str(packet.body)}")

    def on_new_incoming_connection(self, connection: RakNetConnection):
        self.logger.info(f"New Incoming Connection: {str(connection.address)}")

    def on_disconnect(self, connection: RakNetConnection):
        self.logger.info(f"{str(connection.address)} disconnected")

    def on_unknown_packet(self, packet: RakNetFrame, connection: RakNetConnection):
        self.logger.info(f"New Unknown Packet: {str(packet.body)}")

    def start(self):
        self.running = True
        self.raknet_thread.start()
        self.logger.info(f"{self.lang['RUNNING']} ({self.get_time_ms()}s.)")
        self.logger.info(f"{self.lang['PORT']}: {self.port}")
            
    def stop(self):
        self.logger.info(self.lang['STOPPING_WAIT'])
        self.running = False
        self.raknet_server.stop()
        self.raknet_thread.join()
        self.logger.info(self.lang['STOP'])