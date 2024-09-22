import dearpygui.dearpygui as dpg
from systems.loc import Localization as loc


async def manage_users(sender, app_data, user_data) -> None:
    if dpg.does_item_exist("manage_users_window"):
        dpg.focus_item("manage_users_window")
        return

    with dpg.window(
        label=loc.get_string("manage_users_lable"),
        tag="manage_users_window",
        width=400,
        height=200,
        on_close=_on_close
    ):
        pass

def _on_close():
    if dpg.does_item_exist("manage_users_window"):
        dpg.delete_item("manage_users_window")
