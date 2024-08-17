import dearpygui.dearpygui as dpg
from root_path import ROOT_PATH


class FontManager:
    
    @staticmethod
    def load_fonts():
        with dpg.font_registry():
            with dpg.font(str(ROOT_PATH / 'Content' / 'Client' / 'fronts' / 'Monocraft' / 'Monocraft.otf'), 13) as default_font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        
        dpg.bind_font(default_font)
