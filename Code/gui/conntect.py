import logging
from pathlib import Path
import dearpygui.dearpygui as dpg
from DMBotNetwork import Client
from root_path import ROOT_PATH

logger = logging.getLogger("Connect")

class ConnectManager:
    def create_connect_window(self):
        if dpg.does_item_exist("connect_window"):
            dpg.focus_item("connect_window")
            return
        
        with dpg.window(label="Connect", tag="connect_window") as settings_window:
            dpg.add_text("Коннект к серверу")
            
            login = dpg.add_input_text(label="Login")
            password = dpg.add_input_text(label="Password")
            host = dpg.add_input_text(label="Host")
            port = dpg.add_input_int(label="Port")
            
            dpg.add_button(label="SetUp", callback=lambda: self.set_up(login, password, host, port))
            dpg.add_button(label="Connect", callback=self.run_client)

    def set_up(self, login, password, host, port):
        login_value = dpg.get_value(login)
        password_value = dpg.get_value(password)
        host_value = dpg.get_value(host)
        port_value = dpg.get_value(port)

        Client.set_login(login_value)
        Client.set_password(password_value)
        Client.set_host(host_value)
        Client.set_port(port_value)

        server_path = Path(ROOT_PATH) / "Content" / "Servers"
        Client.set_server_file_path(server_path)
        logger.info(f"SetUp done. Path: {server_path}, login: {login_value}, password: {password_value}, host: {host_value}, port: {port_value}")

    async def run_client(self, *args):
        logger.info("Attempting to connect to the server...")
        try:
            await Client.connect()
            logger.info("Connected successfully.")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
