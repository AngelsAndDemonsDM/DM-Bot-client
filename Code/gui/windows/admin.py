import logging
import dearpygui.dearpygui as dpg
from systems.loc import Localization as loc
from DMBotNetwork import Client


async def toggle_access(sender, app_data, user_data):
    user_id = user_data[0]
    access_key = user_data[1]
    new_value = app_data

    changes = {access_key: new_value}
    
    try:
        await Client.req_net_func(
            "change_access", login=user_id, changes=changes
        )
        logging.info(f"Access change for {user_id}: {access_key} -> {new_value}")

    except Exception as e:
        logging.error(f"Failed to update access for {user_id}: {e}")


async def load_user_access(sender, app_data, user_data):
    if dpg.does_item_exist("access_group"):
        dpg.delete_item("access_group")

    if user_data is None:
        logging.error("user_data is None!")
        return

    user: dict[str, bool] = await Client.req_get_data(
        "get_access", None, login=user_data
    )

    if user is None:
        logging.error(f"User '{user_data}' not found.")
        return

    with dpg.group(tag="access_group", parent="access_rights_admin"):
        if "full_access" in user:
            dpg.add_text(loc.get_string("full_access_warning"), wrap=0)
            return

        for access_key, access_value in user.items():
            with dpg.group(horizontal=True, parent="access_group"):
                uuid_text = dpg.generate_uuid()
                dpg.add_text(
                    loc.get_string(f"text-{access_key}"), wrap=0, tag=uuid_text
                )

                dpg.add_checkbox(
                    default_value=access_value,
                    callback=toggle_access,
                    user_data=(user_data, access_key),
                )

                with dpg.popup(uuid_text):
                    dpg.add_text(loc.get_string(f"desc-{access_key}"), wrap=0)

            dpg.add_spacer(width=0, height=10)


async def create_user_control() -> None:
    with dpg.window(
        label=loc.get_string("user_control"),
        width=600,
        height=400,
    ):
        users: list = await Client.req_get_data("get_all_users", None)

        with dpg.group(horizontal=True):
            with dpg.child_window(width=200, autosize_y=True):
                dpg.add_text(loc.get_string("users_control_logins"))
                for user in users:
                    dpg.add_button(
                        label=user, callback=load_user_access, user_data=user
                    )

            with dpg.child_window(
                width=400, tag="access_rights_admin", autosize_y=True, autosize_x=True
            ):
                dpg.add_text(loc.get_string("user_control_access_control"), wrap=0)
                with dpg.group(tag="access_group"):
                    dpg.add_text(loc.get_string("user_control_not_load_user"), wrap=0)
