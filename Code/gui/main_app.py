import dearpygui.dearpygui as dpg
from dearpygui_async import DearPyGuiAsync
from systems.loc import Localization as loc

from .fonts import FontManager


class DMClientApp:
    def __init__(self):
        self.dpg_async = DearPyGuiAsync()

    def setup(self):
        dpg.create_context()
        FontManager.load_fonts()
        dpg.create_viewport(title=loc.get_string("main-app-name"), width=600, height=400)
        dpg.setup_dearpygui()
        self.create_warning_window()

    def create_warning_window(self):
        with dpg.window(label="Warning", modal=True, tag="warning_window"):
            dpg.add_text(loc.get_string("main_text_warning_window"))
            dpg.add_button(label=loc.get_string("yes_warning_window"), callback=self.on_yes)
            dpg.add_button(label=loc.get_string("no_warning_window"), callback=self.on_no)

    def on_yes(self, sender, app_data):
        dpg.delete_item("warning_window")
        self.create_main_window()

    def on_no(self, sender, app_data):
        self.stop()

    def create_main_window(self):
        with dpg.window(label="Main", tag="main_window"):
            pass
    
    def run(self):
        dpg.show_viewport()
        self.dpg_async.run()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def stop(self):
        dpg.stop_dearpygui()
