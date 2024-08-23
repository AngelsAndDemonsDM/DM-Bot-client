import logging

from DMBotNetwork import Client
from gui.main_app import DMClientApp

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app = DMClientApp()
    Client()
    app.setup()
    app.run()
