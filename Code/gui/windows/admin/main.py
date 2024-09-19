import dearpygui.dearpygui as dpg
from systems.loc import Localization as loc

from .manage_server_settings import manage_server_settings
from .manage_users import manage_users
from .user_access_control import user_access_control


async def admin_main_window():
    dpg.add_menu(
        label=loc.get_string("admin_control_menu"),
        tag="admin_control_menu_bar",
        parent="main_bar",
    )

    dpg.add_menu_item(
        label=loc.get_string("user_access_control_lable"),
        parent="admin_control_menu_bar",
        callback=user_access_control,
    )

    dpg.add_menu_item(
        label=loc.get_string("manage_server_settings_lable"),
        parent="admin_control_menu_bar",
        callback=manage_server_settings,
    )

    dpg.add_menu_item(
        label=loc.get_string("manage_users_lable"),
        parent="admin_control_menu_bar",
        callback=manage_users,
    )
