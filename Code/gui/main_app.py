import dearpygui.dearpygui as dpg
from dearpygui_async import DearPyGuiAsync

from .fonts import FontManager
from .settings import SettingsManager


class DMClientApp:
    def __init__(self):
        self.dpg_async = DearPyGuiAsync()

    def setup(self):
        dpg.create_context()
        FontManager.load_fonts()
        dpg.create_viewport(title="DM bot client", width=600, height=400)
        dpg.setup_dearpygui()
        self.create_main_window()

    def create_main_window(self):
        with dpg.window(label="Main", no_title_bar=True) as main_window:
            dpg.add_button(label="Открыть меню настрокек", callback=lambda: SettingsManager.create_settings_window())

    def run(self):
        dpg.show_viewport()
        self.dpg_async.run()

    def cleanup(self):
        dpg.destroy_context()
