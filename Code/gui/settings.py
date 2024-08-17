import dearpygui.dearpygui as dpg
from root_path import ROOT_PATH


class SettingsManager:
    @staticmethod
    def create_settings_window():
        if dpg.does_item_exist("settings_window"):
            dpg.focus_item("settings_window")
            return
        
        with dpg.window(label="Settings", tag="settings_window") as settings_window:
            dpg.add_text("Настройки DM Bot client")
