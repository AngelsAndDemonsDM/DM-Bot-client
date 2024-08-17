from gui.main_app import DMClientApp

if __name__ == "__main__":
    app = DMClientApp()
    app.setup()
    app.run()
    app.cleanup()
