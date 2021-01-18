import bpy
from .functions import fn

class OffsetVert_Panel(bpy.types.Panel):
    bl_idname = "OFFSETVERT_PT_Panel"
    bl_label = "Offset Vertex Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

    # def draw_header(self, context):
    #     layout = self.layout
    #     layout.label(text = "")

    def draw(self, context):
        layout = self.layout
        P = fn.get_user_prefs(bpy.context).addons[__package__].preferences

        layout.row().operator("object.offset_vert_operator", text = "Call operator")

        split = layout.split(factor=0.4)
        split.label(text = "Text Pos")
        split.row().prop(P, "text_pos", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Spacing")
        split.row().prop(P, "line_spacing", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Font Fac")
        split.row().prop(P, "font_fac", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Sensitive")
        split.row().prop(P, "move_sensitive", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Num")
        split.row().prop(P, "color_num", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Num 2")
        split.row().prop(P, "color_num_dark", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Title")
        split.row().prop(P, "color_title", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Title 2")
        split.row().prop(P, "color_sub_title", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Title 3")
        split.row().prop(P, "color_title_dark", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Light")
        split.row().prop(P, "color_highlight", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Panel")
        split.row().prop(P, "color_panel", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Block")
        split.row().prop(P, "color_block", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Block 2")
        split.row().prop(P, "color_block_2", text="")

        split = layout.split(factor=0.5)
        split.label(text = "Color Input")
        split.row().prop(P, "color_block_input", text="")

        layout.row().prop(P, "panel_category")

