import dearpygui.dearpygui as dpg
from systems.loc import Localization as loc


async def manage_users():
    if dpg.does_item_exist("manage_users"):
        dpg.focus_item("manage_users")
        return

    with dpg.window(
        label=loc.get_string("manage_users_lable"),
        tag="manage_users",
        width=400,
        height=200,
    ):
        pass
