from gui.main_app import DMClientApp
from DMBotNetwork import Client

if __name__ == "__main__":
    app = DMClientApp()
    Client()
    app.setup()
    app.run()
    app.cleanup()
