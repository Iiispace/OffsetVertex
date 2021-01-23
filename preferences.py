import bpy
from bpy.props import (
    StringProperty,
    EnumProperty,
    BoolProperty,
    IntProperty,
    IntVectorProperty,
    FloatProperty,
    FloatVectorProperty,
)

from .ui import OffsetVert_Panel
from .keys import *

class OffsetVert_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def update_panel_category(self, context):
        has_panel = hasattr(bpy.types, OffsetVert_Panel.bl_idname)
        if has_panel:
            try:
                bpy.utils.unregister_class(OffsetVert_Panel)
            except:
                pass
        OffsetVert_Panel.bl_category = self.panel_category
        bpy.utils.register_class(OffsetVert_Panel)

    text_pos: IntVectorProperty(
        name = "Text position",
        subtype = 'TRANSLATION',
        size = 2,
        default = (20, 20),
    )

    line_spacing: IntProperty(
        name = "Line spacing",
        default = 30,
        min = -32767, max = 32767,
    )

    font_fac: FloatProperty(
        name = "Font size factor",
        default = 1.0,
        min = 0.0, max = 65535.0,
    )

    move_sensitive: FloatProperty(
        name = "Move sensitive",
        default = 0.0005,
        min = 0.0, max = 1.0,
    )

    color_num: FloatVectorProperty(
        name = "Number color",
        subtype = 'COLOR',
        size = 4,
        default = (1.0, 1.0, 1.0, 0.8),
        min = 0.0, max = 1.0,
    )

    color_num_dark: FloatVectorProperty(
        name = "Number color (Dark)",
        subtype = 'COLOR',
        size = 4,
        default = (0.5, 0.5, 0.5, 0.8),
        min = 0.0, max = 1.0,
    )

    color_title: FloatVectorProperty(
        name = "Title color",
        subtype = 'COLOR',
        size = 4,
        default = (0.8, 0.8, 1.0, 0.8),
        min = 0.0, max = 1.0,
    )

    color_sub_title: FloatVectorProperty(
        name = "Sub title color",
        subtype = 'COLOR',
        size = 4,
        default = (0.95, 0.95, 0.95, 0.8),
        min = 0.0, max = 1.0,
    )

    color_title_dark: FloatVectorProperty(
        name = "Title color (Dark)",
        subtype = 'COLOR',
        size = 4,
        default = (0.53, 0.53, 0.53, 0.8),
        min = 0.0, max = 1.0,
    )

    color_highlight: FloatVectorProperty(
        name = "Highlight color",
        subtype = 'COLOR',
        size = 4,
        default = (1.0, 1.0, 0.0, 0.6),
        min = 0.0, max = 1.0,
    )

    color_panel: FloatVectorProperty(
        name = "Panel color",
        subtype = 'COLOR',
        size = 4,
        default = (0.2, 0.2, 0.2, 0.95),
        min = 0.0, max = 1.0,
    )

    color_block: FloatVectorProperty(
        name = "Block color (Active)",
        subtype = 'COLOR',
        size = 4,
        default = (0.13, 0.13, 0.13, 0.95),
        min = 0.0, max = 1.0,
    )

    color_block_2: FloatVectorProperty(
        name = "Block color",
        subtype = 'COLOR',
        size = 4,
        default = (0.18, 0.18, 0.18, 0.95),
        min = 0.0, max = 1.0,
    )

    color_block_input: FloatVectorProperty(
        name = "Block color (Input)",
        subtype = 'COLOR',
        size = 4,
        default = (0.273, 0.273, 0.273, 0.95),
        min = 0.0, max = 1.0,
    )

    panel_category: StringProperty(
        name = "Category",
        default = "Item",
        update = update_panel_category,
    )

    def draw(self, context):
        # scene = context.scene
        layout = self.layout

        keys = layout.box()
        keys.label(text="Keys")

        self.show_key(keys, key_flip, "Flip Vertex")
        self.show_key(keys, key_reset, "Reset")
        self.show_key(keys, key_minus, "Multiply (-1)")
        self.show_key(keys, key_orientation, "Swap Orientation")
        self.show_key(keys, key_factor_mode, "Swap factor mode")
        self.show_key(keys, key_length_mode, "Swap length mode")
        self.show_key(keys, key_backspace, "Backspace")
        self.show_key(keys, key_confirm, "Confirm")
        self.show_key(keys, key_cancel, "Cancel")

    def show_key(self, box, key, labels):
        key_name = box.box()
        key_name.label(text = labels)
        split = key_name.split(align=True)
        for n in key:
            split.box().column(align = True).label(text = n)
