import dearpygui.dearpygui as dpg
from dearpygui_async import DearPyGuiAsync
from DMBotTools import Coordinate

from .fonts import FontManager
from .map import MapRenderer
from .settings import SettingsManager
from .conntect import ConnectManager

class DMClientApp:
    def __init__(self):
        self.dpg_async = DearPyGuiAsync()

    def setup(self):
        dpg.create_context()
        FontManager.load_fonts()
        dpg.create_viewport(title="DM bot client", width=600, height=400)
        dpg.setup_dearpygui()
        self.create_main_window()
        self.map_renderer = MapRenderer()
        self.connect_manager = ConnectManager()
        
        texture_paths = {
            Coordinate(0, 0): "path/to/texture1.png",
            Coordinate(1, 0): "path/to/texture2.png",
            Coordinate(0, 1): "path/to/texture3.png",
            Coordinate(1, 1): "path/to/nonexistent_texture.png",
            Coordinate(2, 2): "path/to/texture5.png",
        }
        self.map_renderer.set_texture_paths(texture_paths)

    def create_main_window(self):
        with dpg.window(label="Main", no_title_bar=True) as main_window:
            dpg.add_button(label="Открыть меню настроек", callback=lambda: SettingsManager.create_settings_window())
            dpg.add_button(label="Открыть карту", callback=lambda: self.map_renderer.create_map_window())
            dpg.add_button(label="Открыть менеджер присоединения к серверу", callback=lambda: self.connect_manager.create_connect_window())

    def run(self):
        dpg.show_viewport()
        self.dpg_async.run()
        dpg.destroy_context()
