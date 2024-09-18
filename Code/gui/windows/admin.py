import logging
import dearpygui.dearpygui as dpg
from systems.loc import Localization as loc

users = {
    "user1": {
        "change_allow_registration": False,
        "create_users": False,
        "delete_users": True,
        "change_access": False,
        "change_password": True,
    },
    "user2": {
        "change_allow_registration": True,
        "create_users": True,
        "delete_users": False,
        "change_access": True,
        "change_password": False,
    },
    "owner": {"full_access": True},
}


def toggle_access(user_id, access_key, new_value):
    logging.debug(f"User: {user_id}, Access Flag: {access_key}, New Value: {new_value}")


def load_user_access(user_id: str):
    if dpg.does_item_exist("access_group"):
        dpg.delete_item("access_group")

    if user_id is None:
        logging.error("user_id is None!")
        return

    user = users.get(user_id)
    if user is None:
        logging.error(f"User '{user_id}' not found.")
        return

    with dpg.group(tag="access_group", parent="access_rights_admin"):
        if "full_access" in user:
            dpg.add_text(loc.get_string("full_access_warning"), wrap=0)
            return

        for access_key, access_value in user.items():
            with dpg.group(horizontal=True, parent="access_group"):
                uuid = dpg.generate_uuid()
                dpg.add_text(loc.get_string(f"text-{access_key}"), wrap=0, tag=uuid)

                dpg.add_checkbox(
                    default_value=access_value,
                    callback=lambda _, value: toggle_access(user_id, access_key, value),
                )

                with dpg.popup(uuid):
                    dpg.add_text(loc.get_string(f"desc-{access_key}"), wrap=0)

            dpg.add_spacer(width=0, height=10)


def make_button_callback(user):
    def callback(sender, app_data):
        load_user_access(user)

    return callback


async def create_user_control() -> None:
    with dpg.window(label=loc.get_string("user_control"), width=600, height=400):
        with dpg.group(horizontal=True):
            with dpg.child_window(width=200, autosize_y=True):
                dpg.add_text(loc.get_string("users_control_logins"))
                for user in users.keys():
                    dpg.add_button(label=user, callback=make_button_callback(user))

            with dpg.child_window(
                width=400, tag="access_rights_admin", autosize_y=True, autosize_x=True
            ):
                dpg.add_text(loc.get_string("user_control_access_control"), wrap=0)
                with dpg.group(tag="access_group"):
                    dpg.add_text(loc.get_string("user_control_not_load_user"), wrap=0)
