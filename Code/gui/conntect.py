import logging
from pathlib import Path

import dearpygui.dearpygui as dpg
from DMBotNetwork import Client
from root_path import ROOT_PATH
from systems.loc import Localization as loc
from api.chat import ChatModule
logger = logging.getLogger("Connect")

class ConnectManager:
    
    def create_connect_window(self):
        if dpg.does_item_exist("connect_window"):
            dpg.focus_item("connect_window")
            return
        
        with dpg.window(label="Connect", tag="connect_window") as settings_window:
            dpg.add_text(loc.get_string("connect_main_text"))
            
            dpg.add_input_text(hint=loc.get_string("connect_login_hint")   , tag="connect_login")
            dpg.add_input_text(hint=loc.get_string("connect_password_hint"), tag="connect_password", password=True)
            dpg.add_input_text(hint=loc.get_string("connect_host_hint")    , tag="connect_host")
            dpg.add_input_int (label=loc.get_string("connect_port_lable")  , tag="connect_port")
            
            dpg.add_button(label=loc.get_string("connect_button"), callback=self.run_client)
            
            dpg.add_input_text(hint="send_msg_debug", tag="OOC_CHAT")
            dpg.add_button(label="send", callback=self.send_chat_msg)

    async def send_chat_msg(self, *args):
        await ChatModule.send_ooc(dpg.get_value("OOC_CHAT"))

    async def run_client(self, sender, app_data, user_data):
        await Client.close_connection()
        
        login_value = dpg.get_value("connect_login")
        password_value = dpg.get_value("connect_password")
        host_value = dpg.get_value("connect_host")
        port_value = dpg.get_value("connect_port")

        Client.set_login(login_value)
        Client.set_password(password_value)
        Client.set_host(host_value)
        Client.set_port(port_value)

        server_path = Path(ROOT_PATH) / "Content" / "Servers"
        Client.set_server_file_path(server_path)
        logger.info(f"Set up done. Path: {server_path}, login: {login_value}, password: {password_value}, host: {host_value}, port: {port_value}")

        logger.info("Attempting to connect to the server...")
        try:
            await Client.connect()
        
        except Exception as e:
            logger.error(f"Connection failed: {e}")
