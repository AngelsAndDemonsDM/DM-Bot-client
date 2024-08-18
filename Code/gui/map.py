import logging
import os
import time

import dearpygui.dearpygui as dpg
from DMBotTools import Coordinate

logger = logging.getLogger("MapRenderer")

class MapRenderer:
    def __init__(self, cell_size=64, window_width=800, window_height=600):
        self.cell_size = cell_size
        self.window_width = window_width
        self.window_height = window_height
        self.camera_position = Coordinate(0, 0)
        self.textures = {}
        self.texture_paths = {}
        self.is_dragging = False
        self.drag_start_position = Coordinate(0, 0)
        self.initial_camera_position = Coordinate(0, 0)
        self.movement_speed = 0.1 
        self.last_move_time = time.time()
        self.active_keys = set()

    def set_texture_paths(self, texture_dict):
        self.texture_paths = texture_dict

    def load_texture(self, coord):
        if coord not in self.textures:
            path = self.texture_paths.get(coord)
            if path and os.path.exists(path):
                try:
                    width, height, channels, data = dpg.load_image(path)
                    tag = f"texture_{coord.x}_{coord.y}"
                    dpg.add_static_texture(width, height, data, tag=tag)
                    self.textures[coord] = tag
                except Exception as e:
                    logger.error(f"Ошибка загрузки текстуры {path}: {e}")
                    self.textures[coord] = f"Error: {os.path.basename(path)}"
            else:
                logger.warning(f"Текстура не найдена по пути: {path}")
                self.textures[coord] = "No Texture"

    def render_visible_objects(self):
        if not dpg.does_item_exist("map_window"):
            logger.warning("map_window не существует, пропускаем рендеринг.")
            return
        
        if not dpg.does_item_exist("grid_group"):
            with dpg.group(tag="grid_group", parent="map_window"):
                pass

        dpg.delete_item("grid_group", children_only=True)

        for coord in self.texture_paths.keys():
            screen_x = (coord.x - self.camera_position.x) * self.cell_size
            screen_y = (coord.y - self.camera_position.y) * self.cell_size

            if 0 <= screen_x < self.window_width and 0 <= screen_y < self.window_height:
                self.load_texture(coord)
                texture_tag = self.textures[coord]
                if texture_tag.startswith("texture_"):
                    dpg.add_image(texture_tag, pos=(screen_x, screen_y), parent="grid_group")
                else:
                    dpg.add_text(texture_tag, pos=(screen_x, screen_y), parent="grid_group")

    def create_map_window(self):
        if dpg.does_item_exist("map_window"):
            dpg.focus_item("map_window")
            return

        with dpg.window(label="Map Renderer", tag="map_window", width=self.window_width, height=self.window_height):
            with dpg.handler_registry():
                dpg.add_key_press_handler(callback=self.key_down_callback)
                dpg.add_key_release_handler(callback=self.key_up_callback)
                dpg.add_mouse_drag_handler(button=dpg.mvMouseButton_Left, callback=self.on_mouse_drag)
                dpg.add_mouse_release_handler(button=dpg.mvMouseButton_Left, callback=self.on_mouse_release)

        self.render_visible_objects()

    def on_mouse_drag(self, sender, app_data):
        if not self.is_dragging:
            self.is_dragging = True
            self.drag_start_position = Coordinate(app_data[1], app_data[2])
            self.initial_camera_position = self.camera_position

        delta_x = (self.drag_start_position.x - app_data[1]) // self.cell_size
        delta_y = (self.drag_start_position.y - app_data[2]) // self.cell_size
        self.camera_position = self.initial_camera_position + Coordinate(delta_x, delta_y)
        
        if dpg.does_item_exist("grid_group"):
            self.render_visible_objects()

    def move_camera_slow(self, dx, dy):
        current_time = time.time()
        if current_time - self.last_move_time > self.movement_speed:
            self.camera_position += Coordinate(dx, dy)
            self.render_visible_objects()
            self.last_move_time = current_time

    def key_down_callback(self, sender, app_data):
        self.active_keys.add(app_data)
        self.process_movement()

    def key_up_callback(self, sender, app_data):
        self.active_keys.discard(app_data)

    def process_movement(self):
        dx = dy = 0
        if dpg.mvKey_W in self.active_keys:
            dy -= 1
        if dpg.mvKey_S in self.active_keys:
            dy += 1
        if dpg.mvKey_A in self.active_keys:
            dx -= 1
        if dpg.mvKey_D in self.active_keys:
            dx += 1

        if dx != 0 or dy != 0:
            self.move_camera_slow(dx, dy)

    def on_mouse_release(self, sender, app_data):
        self.is_dragging = False
