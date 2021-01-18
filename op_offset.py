import bpy, blf, bgl, gpu, bmesh, math
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

from .functions import fn

font_id = 1
mouse_flip_region = 50
delta = 0

key_confirm = {'LEFTMOUSE', 'RET', 'NUMPAD_ENTER'}
key_cancel = {'RIGHTMOUSE', 'ESC'}
key_1 = {'ONE', 'NUMPAD_1'}
key_2 = {'TWO', 'NUMPAD_2'}
key_3 = {'THREE', 'NUMPAD_3'}
key_4 = {'FOUR', 'NUMPAD_4'}
key_5 = {'FIVE', 'NUMPAD_5'}
key_6 = {'SIX', 'NUMPAD_6'}
key_7 = {'SEVEN', 'NUMPAD_7'}
key_8 = {'EIGHT', 'NUMPAD_8'}
key_9 = {'NINE', 'NUMPAD_9'}
key_0 = {'ZERO', 'NUMPAD_0'}
key_dot = {'PERIOD', 'NUMPAD_PERIOD'}
key_minus = {'MINUS'}
key_backspace = {'BACK_SPACE'}
key_up = {'UP_ARROW'}
key_down = {'DOWN_ARROW'}
key_left = {'LEFT_ARROW'}
key_right = {'RIGHT_ARROW'}
key_star = {'NUMPAD_ASTERIX'}
key_factor_mode = {'NUMPAD_ASTERIX', 'F'}
key_length_mode = {'SLASH', 'NUMPAD_SLASH', 'D'}
key_slash = {'SLASH', 'NUMPAD_SLASH'}
key_flip = {'MIDDLEMOUSE', 'G', 'S'}
key_reset = {'R'}
key_copy = {'C'}
key_orientation = {'O', 'T'}

class OffsetVert_Offset(bpy.types.Operator):
    bl_idname = "object.offset_vert_operator"
    bl_label = "Offset Vertex Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.def_modal = self.if_modal
        self.def_mode = self.if_mode_offset
        self.def_drag = self.if_drag_do
        self.def_dragged = self.if_dragged
        
        self.def_swap_orientation = self.if_swap_orientation_local
        self.def_return_length_from_offset = self.if_return_length_from_offset_local
        self.def_return_factor_from_length = self.if_return_factor_from_length_local
        self.def_return_offset_from_factor = self.if_return_offset_from_factor_local

        self.def_draw = self.draw_callback_px

        
    def invoke(self, context, event):
        if not context.area.type == 'VIEW_3D':
            return {'CANCELLED'}
        if not context.object.mode == 'EDIT':
            self.report({'WARNING'}, "Edit Mode only")
            return {'CANCELLED'}
        if not context.object:
            self.report({'WARNING'}, "No active object, cancelled")
            return {'CANCELLED'}

        self.P = fn.get_user_prefs(bpy.context).addons[__package__].preferences
        self.mouse_x_last = event.mouse_x
        self.mouse_x_offset = 0
        self.win_height_half = context.window.height //2
        self.win_width_half = context.window.width //2
        self.sensitive = self.P.move_sensitive *context.space_data.region_3d.view_distance

        self.obj = context.edit_object
        self.bm = bmesh.from_edit_mesh(self.obj.data)
        self.bm_copy = self.bm.copy()

        self.sel_vert_el = fn.get_selected_vert(self.bm)
        self.act_el = fn.get_active_vertex_elem(self.bm)
        self.org_el = fn.get_selected_vert(self.bm_copy)

        self.mode = "Two Points"
        self.offset = 0.0
        self.length = 0.0
        self.factor = 1.0
        self.input_text = ""
        self.input_text_last = ""


        if len(self.sel_vert_el) == 2:              # decide mode
            if self.act_el == None:
                self.mode = "Two Points - No Active"
        elif len(self.sel_vert_el) > 2:
            if self.act_el == None:
                self.report({'WARNING'}, "2 vertices only if no active point !")
                return {'CANCELLED'}
            self.mode = "Multi Points - From Active"
        else:
            self.report({'WARNING'}, "At least select 2 Vertices !")
            return {'CANCELLED'}

        # Get direction
        if self.mode in {"Two Points", "Two Points - No Active"}:
            self.clean_line()

            self.calc_blf_size()
            self.calc_blf_pos_x()
            self.calc_blf_pos_y()
            self.calc_background_rec()

            self.line[3][1] = self.mode
            self.get_color()

            if context.scene.transform_orientation_slots[0].type != 'LOCAL':
                self.def_swap_orientation()
            else:
                self.line[4][1] = "Local"

            if self.act_el != self.sel_vert_el[0]:
                self.direction = self.sel_vert_el[1].co - self.sel_vert_el[0].co
                self.move_ind = 1
            else:
                self.direction = self.sel_vert_el[0].co - self.sel_vert_el[1].co
                self.move_ind = 0
            self.direction_nor = self.direction.normalized()
            self.direction_length = self.direction.length
            # self.direction_nor_world = self.direction_nor *(self.obj.matrix_world.inverted_safe() @ self.direction_nor).length
            self.direction_world_length = (self.obj.matrix_world @ self.direction).length
            self.line[0][1] = fn.format_str("0")
            self.line[1][1] = fn.format_f(self.def_return_length_from_offset())
            self.line[2][1] = fn.format_str("1")
            self.sensitive_fac = self.sensitive / self.direction_world_length

        else:
            self.multi_factor = 0.0
            self.def_mode = self.if_mode_multi
            self.def_dragged = self.if_multi_dragged
            self.def_draw = self.draw_callback_px_multi
            self.clean_line_multi()

            self.calc_blf_size()
            self.calc_blf_pos_x()
            self.calc_blf_pos_y()
            self.calc_background_rec()

            self.line[3][1] = self.mode
            self.line[0][1] = fn.format_str("0")
            self.line[1][1] = "           N/A"
            self.get_color()
            self.line_color[2] = [self.P.color_title, self.P.color_sub_title]
            spac = self.P.line_spacing
            font_fac = self.P.font_fac
            self.blf_pos_y[2] = int(self.blf_pos_y[1] + spac * font_fac)
            self.blf_pos_y[3] = int(self.blf_pos_y[2] + spac * 0.7 * font_fac)
            self.blf_pos_y[4] = int(self.blf_pos_y[3] + spac * 0.7 * font_fac)
            self.background_rec[3] = self.P.text_pos[1] + (15 + spac * 3.75) * font_fac
            self.blf_multi_pos_x_sp = int(self.P.text_pos[0] + 139 * font_fac)

            if context.scene.transform_orientation_slots[0].type != 'LOCAL':
                self.def_multi_swap_orientation()
            else:
                self.line[4][1] = "Local"

            self.direction = []
            self.direction_nor = []
            self.direction_nor_world = []

            for v in self.sel_vert_el:
                vec = v.co - self.act_el.co
                vec_nor = vec.normalized()
                world_fac = (self.obj.matrix_world.inverted_safe() @ vec_nor).length
                self.direction.append(vec)
                self.direction_nor.append(vec_nor)
                self.direction_nor_world.append(vec_nor * world_fac)

            self.len_el = len(self.direction)
            ave_length = (
                (self.obj.matrix_world @ self.direction[self.len_el-1]).length
                +(self.obj.matrix_world @ self.direction[self.len_el>>1]).length
                +(self.obj.matrix_world @ self.direction[self.len_el>>2]).length
                +(self.obj.matrix_world @ self.direction[self.len_el>>3]).length
            )/4.0
            self.sensitive_fac = self.sensitive / ave_length
            self.line[2][1] = str(self.len_el)

        self._handle = bpy.types.SpaceView3D.draw_handler_add(
            self.def_draw, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        context.window.cursor_set('SCROLL_X')
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    # ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ Modal
    def modal(self, context, event):
        return self.def_modal(context, event)

    # ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ Draw
    def draw_callback_px(self, context):
        self.draw_rec(self.background_rec, self.P.color_panel)
        self.draw_rec(self.rec_offset, self.rec_color_offset)
        self.draw_rec(self.rec_length, self.rec_color_length)
        self.draw_rec(self.rec_factor, self.rec_color_factor)

        # ====================================================================== 0
        self.use_color(self.line_color[0][0]) # Offset
        self.use_size(0)
        self.use_pos_draw(0, 0, 0, 0)

        self.use_color(self.line_color[0][1])
        self.use_pos_draw(1, 0, 0, 1)
        # ----------------------------------------------------------------- 1
        self.use_color(self.line_color[1][0]) # Length
        self.use_size(0)
        self.use_pos_draw(0, 1, 1, 0)

        self.use_color(self.line_color[1][1])
        self.use_pos_draw(1, 1, 1, 1)
        # ----------------------------------------------------------------- 2
        self.use_color(self.line_color[2][0]) # Factor
        self.use_size(0)
        self.use_pos_draw(0, 2, 2, 0)

        self.use_color(self.line_color[2][1])
        self.use_pos_draw(1, 2, 2, 1)
        # ----------------------------------------------------------------- 3
        self.use_color(self.line_color[3][0])
        self.use_size(1)
        self.use_pos_draw(0, 3, 3, 0)

        self.use_color(self.line_color[3][1])
        self.use_pos_draw(2, 3, 3, 1)

        self.use_color(self.line_color[3][2])
        self.use_pos_draw(3, 3, 3, 2)
        # ----------------------------------------------------------------- 4
        self.use_color(self.line_color[4][0])
        self.use_pos_draw(0, 4, 4, 0)

        self.use_color(self.line_color[4][1])
        self.use_pos_draw(4, 4, 4, 1)

    def use_color(self, c):
        blf.color(font_id, c[0], c[1], c[2], c[3])
        
    def use_size(self, ind):
        blf.size(font_id, self.blf_size[ind], 72)

    def use_pos_draw(self, ind_x, ind_y, ind_line_up, ind_line_right):
        blf.position(font_id, self.blf_pos_x[ind_x], self.blf_pos_y[ind_y], 0)
        blf.draw(font_id, self.line[ind_line_up][ind_line_right])

    # ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def clean_line(self):
        self.line = [
            ["Offset:", ""],
            ["Length:", ""],
            ["Factor:", ""],
            ["Mode:", "", ""],
            ["Orientation:", ""],
        ]
    def clean_line_multi(self):
        self.line = [
            ["Offset:", ""],
            ["Factor:", ""],
            ["Vertices selected:", "", ""],
            ["Mode:", "", ""],
            ["Orientation:", ""],
        ]

    def get_color(self):
        self.line_color = [
            [self.P.color_title, self.P.color_num],
            [self.P.color_title_dark, self.P.color_num_dark],
            [self.P.color_title_dark, self.P.color_num_dark],
            [self.P.color_title, self.P.color_sub_title, self.P.color_highlight],
            [self.P.color_title, self.P.color_sub_title]
        ]
        self.rec_color_offset = self.P.color_block
        self.rec_color_length = self.P.color_block_2
        self.rec_color_factor = self.P.color_block_2

    def calc_blf_size(self):
        self.blf_size = [0]*3
        
        self.blf_size[0] = int(16 * self.P.font_fac)
        self.blf_size[1] = int(13 * self.P.font_fac)

    def calc_blf_pos_x(self):
        self.blf_pos_x = [0]*5
        x = self.P.text_pos[0]
        fac = self.P.font_fac

        self.blf_pos_x[0] = int(x)
        self.blf_pos_x[1] = int(x + 70 * fac)
        self.blf_pos_x[2] = int(x + 50 * fac)
        self.blf_pos_x[3] = int(x + 219 * fac)
        self.blf_pos_x[4] = int(x + 99 * fac)

    def calc_blf_pos_y(self):
        self.blf_pos_y = [0]*5
        y = self.P.text_pos[1]
        spac = self.P.line_spacing

        self.blf_pos_y[0] = int(y)
        self.blf_pos_y[1] = int(self.blf_pos_y[0] + spac * self.P.font_fac)
        self.blf_pos_y[2] = int(self.blf_pos_y[1] + spac * self.P.font_fac)
        self.blf_pos_y[3] = int(self.blf_pos_y[2] + spac * self.P.font_fac)
        self.blf_pos_y[4] = int(self.blf_pos_y[3] + spac * 0.7 * self.P.font_fac)

    def calc_background_rec(self):
        x = self.P.text_pos[0]
        y = self.P.text_pos[1]
        fac = self.P.font_fac
        spac = self.P.line_spacing
        offset = 15

        self.background_rec = [
            x - offset *fac,
            x + 310 * fac,
            y - offset *fac,
            y + (offset + spac * 4.05) * fac
        ]

        self.rec_offset = [
            self.background_rec[0] + 83 * fac,
            self.background_rec[1] - 9 * fac,
            y - 6 * fac,
            y + 18 * fac
        ]

        self.rec_length = [
            self.rec_offset[0],
            self.rec_offset[1],
            self.rec_offset[2] + spac * fac,
            self.rec_offset[3] + spac * fac
        ]

        self.rec_factor = [
            self.rec_length[0],
            self.rec_length[1],
            self.rec_length[2] + spac * fac,
            self.rec_length[3] + spac * fac
        ]

    def draw_rec(self, rec, color):
        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        self.shader.bind()
        self.shader.uniform_float("color", color)

        vert = ((rec[0], rec[2]), (rec[0], rec[3]), (rec[1], rec[3]), (rec[1], rec[2]))
        
        bgl.glEnable(bgl.GL_BLEND)
        self.batch_panel = batch_for_shader(
            self.shader, 'TRIS', {"pos" : vert},
            indices=((0, 1, 2), (0, 2, 3)))
        self.batch_panel.draw(self.shader)
        bgl.glDisable(bgl.GL_BLEND)

    def free(self, context):
        self.bm_copy.free()
        del self.org_el
        context.window.cursor_set('CROSSHAIR')

# ▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_modal_fin(self, context, event):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self.free(context)
        context.area.tag_redraw()
        return {'FINISHED'}

    def if_modal_cancel(self, context, event):
        bpy.ops.object.mode_set(mode='OBJECT')
        self.bm_copy.to_mesh(self.obj.data)
        bpy.ops.object.mode_set(mode='EDIT')
        bmesh.update_edit_mesh(self.obj.data, True)
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self.free(context)
        return {'CANCELLED'}

    def if_modal(self, context, event):
        self.def_mode(context, event)
        
        return {'RUNNING_MODAL'}

    def if_mode_offset(self, context, event):
        self.def_drag(context, event)
# __  ________________________________________________________________        
# ▇__▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_drag_do(self, context, event):
        self.get_key_inOffsetDrag(context, event)
        # if mouse move: to self.offset, line , remesh (if need)
        self.def_dragged(context, event)
    def if_drag_stop(self, context, event):
        self.get_key_inOffsetDirect(context, event)
# __  __  ____________________________________________________________
# ▇__▇__▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_dragged(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = event.mouse_x - self.mouse_x_last
            if math.fabs(delta) < self.win_width_half:
                self.mouse_x_offset += delta
                self.offset = round(self.mouse_x_offset *self.sensitive, 3)
                self.line[0][1] = fn.format_f(self.offset)
                self.length = self.def_return_length_from_offset()
                self.line[1][1] = fn.format_f(self.length)
                self.factor = self.def_return_factor_from_length()
                self.line[2][1] = fn.format_f(self.factor)
                self.fac_remesh()
                bmesh.update_edit_mesh(self.obj.data, True)
            self.loop_mouse(context, event)
    def if_dragged_stop(self, context, event):
        self.line[0][1] = fn.format_str(self.input_text)
        self.length = self.def_return_length_from_offset()
        self.line[1][1] = fn.format_f(self.length)
        self.factor = self.def_return_factor_from_length()
        self.line[2][1] = fn.format_f(self.factor)
        self.fac_remesh()
        bmesh.update_edit_mesh(self.obj.data, True)
# __  __  __  ________________________________________________________

    def get_key_inOffsetDrag(self, context, event):
        if event.value != 'PRESS':
            return

        if event.type in key_confirm:
            self.def_modal = self.if_modal_fin
            return
        elif event.type in key_cancel:
            self.def_modal = self.if_modal_cancel
            return
        elif event.type in key_0:
            self.offset = 0.0
            self.input_text = "0"
        elif event.type in key_1:
            self.offset = 1.0
            self.input_text = "1"
        elif event.type in key_2:
            self.offset = 2.0
            self.input_text = "2"
        elif event.type in key_3:
            self.offset = 3.0
            self.input_text = "3"
        elif event.type in key_4:
            self.offset = 4.0
            self.input_text = "4"
        elif event.type in key_5:
            self.offset = 5.0
            self.input_text = "5"
        elif event.type in key_6:
            self.offset = 6.0
            self.input_text = "6"
        elif event.type in key_7:
            self.offset = 7.0
            self.input_text = "7"
        elif event.type in key_8:
            self.offset = 8.0
            self.input_text = "8"
        elif event.type in key_9:
            self.offset = 9.0
            self.input_text = "9"
        elif event.type in key_dot:
            self.offset = 0.0
            self.input_text = "0."
        elif event.type in key_minus:
            self.offset = 0.0
            self.input_text = "-"
        elif event.type in key_flip:
            self.flip_vert()
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_reset:
            self.offset = 0.0
            self.factor = 1.0
            self.mouse_x_offset = 0
            self.line[0][1] = fn.format_str("0")
            self.line[1][1] = fn.format_f(self.def_return_length_from_offset())
            self.line[2][1] = fn.format_str("1")
            self.reset_vert()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_backspace:
            self.input_text = fn.str_f(self.offset)
            self.input_text = self.input_text[:-1]
            self.offset = fn.try_str_to_float(self.input_text)
        elif event.type in key_orientation:
            self.def_swap_orientation()
            self.length = self.def_return_length_from_offset()
            self.line[1][1] = fn.format_f(self.length)
            self.factor = self.def_return_factor_from_length()
            self.line[2][1] = fn.format_f(self.factor)
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_factor_mode:
            self.def_mode = self.if_mode_fac
            self.def_fac_drag = self.if_fac_drag_do
            self.def_dragged = self.if_fac_dragged
            self.factor = round(self.mouse_x_offset * self.sensitive, 3)
            self.mouse_x_offset = self.factor / self.sensitive_fac
            self.line[2][1] = fn.format_f(self.factor)
            self.offset = self.def_return_offset_from_factor()
            self.line[0][1] = fn.format_f(self.offset)
            self.line[1][1] = fn.format_f(self.def_return_length_from_offset())
            self.line_color[0][0] = self.P.color_title_dark
            self.line_color[0][1] = self.P.color_num_dark
            self.line_color[2][0] = self.P.color_title
            self.line_color[2][1] = self.P.color_num
            self.rec_color_offset = self.P.color_block_2
            self.rec_color_factor = self.P.color_block
            self.line[3][2] = "Factor mode"
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_length_mode:
            self.def_mode = self.if_mode_length
            self.def_length_drag = self.if_length_drag_do
            self.def_dragged = self.if_length_dragged
            self.length = round(self.mouse_x_offset * self.sensitive, 3)
            self.mouse_x_offset = self.length / self.sensitive
            self.line[1][1] = fn.format_f(self.length)
            self.factor = self.def_return_factor_from_length()
            self.line[2][1] = fn.format_f(self.factor)
            self.offset = self.def_return_offset_from_factor()
            self.line[0][1] = fn.format_f(self.offset)
            self.line_color[0][0] = self.P.color_title_dark
            self.line_color[0][1] = self.P.color_num_dark
            self.line_color[1][0] = self.P.color_title
            self.line_color[1][1] = self.P.color_num
            self.rec_color_offset = self.P.color_block_2
            self.rec_color_length = self.P.color_block
            self.line[3][2] = "Length mode"
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        else:
            return
        # press [0123456789.-][backspace]: through here
        self.input_text_last = self.input_text
        self.def_drag = self.if_drag_stop
        self.def_dragged = self.if_dragged_stop
        context.window.cursor_set('CROSSHAIR')
        self.rec_color_offset = self.P.color_block_input
        
    def get_key_inOffsetDirect(self, context, event):
        if event.value != 'PRESS':
            return

        if event.type in key_confirm:
            self.def_modal = self.if_modal_fin
            return
        elif event.type in key_cancel:
            self.def_modal = self.if_modal_cancel
            return
        elif event.type in key_0:
            if self.input_text in {"0", "-0"}:
                return
            self.input_text += "0"
        elif event.type in key_1:
            if self.input_text in {"0", "-0"}:
                self.input_text = self.input_text[:-1] + "1"
            else:
                self.input_text += "1"
        elif event.type in key_2:
            if self.input_text in {"0", "-0"}:
                self.input_text = self.input_text[:-1] + "2"
            else:
                self.input_text += "2"
        elif event.type in key_3:
            if self.input_text in {"0", "-0"}:
                self.input_text = self.input_text[:-1] + "3"
            else:
                self.input_text += "3"
        elif event.type in key_4:
            if self.input_text in {"0", "-0"}:
                self.input_text = self.input_text[:-1] + "4"
            else:
                self.input_text += "4"
        elif event.type in key_5:
            if self.input_text in {"0", "-0"}:
                self.input_text = self.input_text[:-1] + "5"
            else:
                self.input_text += "5"
        elif event.type in key_6:
            if self.input_text in {"0", "-0"}:
                self.input_text = self.input_text[:-1] + "6"
            else:
                self.input_text += "6"
        elif event.type in key_7:
            if self.input_text in {"0", "-0"}:
                self.input_text = self.input_text[:-1] + "7"
            else:
                self.input_text += "7"
        elif event.type in key_8:
            if self.input_text in {"0", "-0"}:
                self.input_text = self.input_text[:-1] + "8"
            else:
                self.input_text += "8"
        elif event.type in key_9:
            if self.input_text in {"0", "-0"}:
                self.input_text = self.input_text[:-1] + "9"
            else:
                self.input_text += "9"
        elif event.type in key_dot:
            if self.input_text == "":
                self.input_text = "0."
            elif self.input_text == "-":
                self.input_text = "-0."
            else:
                self.input_text += "."
        elif event.type in key_minus:
            if self.input_text[:1] == "-":
                self.input_text = self.input_text[1:]
            else:
                self.input_text = "-" + self.input_text
        elif event.type in key_flip:
            self.flip_vert()
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_reset:
            context.window.cursor_set('SCROLL_X')
            self.offset = 0.0
            self.factor = 1.0
            self.mouse_x_offset = 0
            self.mouse_x_last = event.mouse_x
            self.line[0][1] = fn.format_str("0")
            self.line[1][1] = fn.format_f(self.def_return_length_from_offset())
            self.line[2][1] = fn.format_str("1")
            self.rec_color_offset = self.P.color_block
            self.reset_vert()
            bmesh.update_edit_mesh(self.obj.data, True)
            self.def_drag = self.if_drag_do
            self.def_dragged = self.if_dragged
            return
        elif event.type in key_backspace:
            self.input_text = self.input_text[:-1]
            self.offset = fn.try_str_to_float(self.input_text)
            self.input_text_last = self.input_text
            self.if_dragged_stop(context, event) # remesh, update line
            return
        elif event.type in key_orientation:
            self.def_swap_orientation()
            self.length = self.def_return_length_from_offset()
            self.line[1][1] = fn.format_f(self.length)
            self.factor = self.def_return_factor_from_length()
            self.line[2][1] = fn.format_f(self.factor)
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_factor_mode:
            self.def_mode = self.if_mode_fac
            self.def_fac_drag = self.if_fac_drag_stop
            self.def_dragged = self.if_fac_dragged_stop
            self.factor = fn.try_str_to_float(self.input_text)
            self.line[2][1] = fn.format_str(self.input_text)
            self.offset = self.def_return_offset_from_factor()
            self.line[0][1] = fn.format_f(self.offset)
            self.line[1][1] = fn.format_f(self.def_return_length_from_offset())
            self.line_color[0][0] = self.P.color_title_dark
            self.line_color[0][1] = self.P.color_num_dark
            self.line_color[2][0] = self.P.color_title
            self.line_color[2][1] = self.P.color_num
            self.rec_color_offset = self.P.color_block_2
            self.rec_color_factor = self.P.color_block_input
            self.line[3][2] = "Factor mode"
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_length_mode:
            self.def_mode = self.if_mode_length
            self.def_length_drag = self.if_length_drag_stop
            self.def_dragged = self.if_length_dragged_stop
            self.length = fn.try_str_to_float(self.input_text)
            self.line[1][1] = fn.format_str(self.input_text)
            self.factor = self.def_return_factor_from_length()
            self.line[2][1] = fn.format_f(self.factor)
            self.line[0][1] = fn.format_f(self.def_return_offset_from_factor())

            self.line_color[0][0] = self.P.color_title_dark
            self.line_color[0][1] = self.P.color_num_dark
            self.line_color[1][0] = self.P.color_title
            self.line_color[1][1] = self.P.color_num
            self.rec_color_offset = self.P.color_block_2
            self.rec_color_length = self.P.color_block_input
            self.line[3][2] = "Length mode"
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        else:
            return
        # press [0123456789.-]: through here
        try_to_float = fn.try_str_to_float(self.input_text)
        if try_to_float == None:
            self.input_text = self.input_text_last
        else:
            if self.input_text[:1] == "-":
                if len(self.input_text) - 1 > 14:
                    self.input_text = self.input_text_last
                    return
            else:
                if len(self.input_text) - 1 > 13:
                    self.input_text = self.input_text_last
                    return

            self.input_text_last = self.input_text
            self.offset = try_to_float
            self.if_dragged_stop(context, event) # remesh, update line


    def reset_vert(self):
        self.sel_vert_el[self.move_ind].co = self.org_el[self.move_ind].co
        self.sel_vert_el[1-self.move_ind].co = self.org_el[1-self.move_ind].co

    def flip_vert(self):
        self.direction *= -1
        self.direction_nor *= -1
        # self.direction_nor_world *= -1
        self.reset_vert()
        self.move_ind = 1 - self.move_ind
        
    def if_swap_orientation_local(self):
        self.def_swap_orientation = self.if_swap_orientation_unlocal
        self.def_return_offset_from_factor = self.if_return_offset_from_factor_unlocal
        self.def_return_factor_from_length = self.if_return_factor_from_length_unlocal
        self.def_return_length_from_offset = self.if_return_length_from_offset_unlocal
        self.line[4][1] = "Global"
    def if_swap_orientation_unlocal(self):
        self.def_swap_orientation = self.if_swap_orientation_local
        self.def_return_offset_from_factor = self.if_return_offset_from_factor_local
        self.def_return_factor_from_length = self.if_return_factor_from_length_local
        self.def_return_length_from_offset = self.if_return_length_from_offset_local
        self.line[4][1] = "Local"

    def loop_mouse(self, context, event):
        if event.mouse_x < mouse_flip_region:
            new_x = context.window.width - mouse_flip_region - 30
            context.window.cursor_warp(new_x, self.win_height_half)
            self.mouse_x_last = new_x
        elif event.mouse_x > context.window.width - mouse_flip_region:
            new_x = mouse_flip_region + 30
            context.window.cursor_warp(new_x, self.win_height_half)
            self.mouse_x_last = new_x
        else:
            self.mouse_x_last = event.mouse_x

    def if_return_length_from_offset_local(self):
        return self.direction_length + self.offset
    def if_return_length_from_offset_unlocal(self):
        return self.direction_world_length + self.offset

    def if_return_factor_from_length_local(self):
        return self.length / self.direction_length
    def if_return_factor_from_length_unlocal(self):
        return self.length / self.direction_world_length

    def if_return_offset_from_factor_local(self):
        return self.direction_length * (self.factor-1)
    def if_return_offset_from_factor_unlocal(self):
        return self.direction_world_length * (self.factor-1)


    def fac_remesh(self):
        self.sel_vert_el[self.move_ind].co = self.org_el[self.move_ind].co + (
            self.direction *(self.factor - 1)
        )