from .server import BedrockServer

if __name__ == '__main__':
    server = BedrockServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.logger.info('Stopping...')
        server.stop()