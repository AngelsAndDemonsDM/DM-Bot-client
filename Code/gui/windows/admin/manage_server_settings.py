import dearpygui.dearpygui as dpg
from systems.loc import Localization as loc


async def manage_server_settings():
    if dpg.does_item_exist("manage_server_settings"):
        dpg.focus_item("manage_server_settings")
        return

    with dpg.window(
        label=loc.get_string("manage_server_settings_lable"),
        tag="manage_server_settings",
        width=400,
        height=200,
    ):
        pass
