from .op_length import *

class OffsetVert_Multi(OffsetVert_Length):
    bl_idname = "object.offset_vert_operator"
    bl_label = "Offset Vertex Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):        
        super().__init__()

        self.def_multi_drag = self.if_multi_drag_do
        self.def_remesh = self.if_remesh_local
        self.def_multi_swap_orientation = self.if_multi_swap_orientation_local

     # ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ Draw
    def draw_callback_px_multi(self, context):
        self.draw_rec(self.background_rec, self.P.color_panel)
        self.draw_rec(self.rec_offset, self.rec_color_offset)
        self.draw_rec(self.rec_length, self.rec_color_length)

        # ====================================================================== 0
        self.use_color(self.line_color[0][0]) # Offset
        self.use_size(0)
        self.use_pos_draw(0, 0, 0, 0)

        self.use_color(self.line_color[0][1])
        self.use_pos_draw(1, 0, 0, 1)
        # ----------------------------------------------------------------- 1
        self.use_color(self.line_color[1][0]) # Factor
        self.use_size(0)
        self.use_pos_draw(0, 1, 1, 0)

        self.use_color(self.line_color[1][1])
        self.use_pos_draw(1, 1, 1, 1)
        # ----------------------------------------------------------------- 2
        self.use_color(self.line_color[2][0])
        self.use_size(1)
        self.use_pos_draw(0, 2, 2, 0)

        self.use_color(self.line_color[2][1])
        blf.position(font_id, self.blf_multi_pos_x_sp, self.blf_pos_y[2], 0)
        blf.draw(font_id, self.line[2][1])

        self.use_color(self.line_color[3][2])
        blf.position(font_id, self.blf_pos_x[3], self.blf_pos_y[2], 0)
        blf.draw(font_id, self.line[2][2])
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

# ▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_mode_multi(self, context, event):
        self.def_multi_drag(context, event)
# __  ________________________________________________________________
# ▇__▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_multi_drag_do(self, context, event):
        self.get_key_inMultiDrag(context, event)
        # if mouse move: to self.offset, line , remesh (if need)
        self.def_dragged(context, event)
    def if_multi_drag_stop(self, context, event):
        self.get_key_inMultiDirect(context, event)
# __  __  ____________________________________________________________
# ▇__▇__▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_multi_dragged(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = event.mouse_x - self.mouse_x_last
            if math.fabs(delta) < self.win_width_half:
                self.mouse_x_offset += delta
                self.offset = round(self.mouse_x_offset *self.sensitive, 3)
                self.line[0][1] = fn.format_f(self.offset)
                
                self.def_remesh()
                bmesh.update_edit_mesh(self.obj.data, True)
            self.loop_mouse(context, event)
    def if_multi_dragged_stop(self, context, event):
        self.line[0][1] = fn.format_str(self.input_text)
        self.def_remesh()
        bmesh.update_edit_mesh(self.obj.data, True)
# __  __  __  ________________________________________________________

    def get_key_inMultiDrag(self, context, event):
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
        elif event.type in key_reset:
            self.offset = 0.0
            self.mouse_x_offset = 0
            self.line[0][1] = fn.format_str("0")
            self.def_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_backspace:
            self.input_text = fn.str_f(self.offset)
            self.input_text = self.input_text[:-1]
            self.offset = fn.try_str_to_float(self.input_text)
        elif event.type in key_orientation:
            self.def_multi_swap_orientation()
            self.def_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_factor_mode:
            self.def_mode = self.if_mode_multi_fac
            self.def_multi_drag = self.if_multi_fac_drag_do
            self.def_dragged = self.if_multi_fac_dragged
            self.factor = round(self.mouse_x_offset * self.sensitive, 3)
            self.mouse_x_offset = self.factor / self.sensitive_fac
            self.line[1][1] = fn.format_f(self.factor)
            self.line[0][1] = "           N/A"

            self.line_color[0][0] = self.P.color_title_dark
            self.line_color[0][1] = self.P.color_num_dark
            self.line_color[1][0] = self.P.color_title
            self.line_color[1][1] = self.P.color_num
            self.rec_color_offset = self.P.color_block_2
            self.rec_color_length = self.P.color_block
            self.line[2][2] = "Factor mode"
            self.multi_fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        else:
            return
        # press [0123456789.-][backspace]: through here
        self.input_text_last = self.input_text
        self.def_multi_drag = self.if_multi_drag_stop
        self.def_dragged = self.if_multi_dragged_stop
        context.window.cursor_set('CROSSHAIR')
        self.rec_color_offset = self.P.color_block_input

    def get_key_inMultiDirect(self, context, event):
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
        elif event.type in key_reset:
            context.window.cursor_set('SCROLL_X')
            self.offset = 0.0
            self.mouse_x_offset = 0
            self.mouse_x_last = event.mouse_x
            self.line[0][1] = fn.format_str("0")
            self.rec_color_offset = self.P.color_block
            self.def_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            self.def_multi_drag = self.if_multi_drag_do
            self.def_dragged = self.if_multi_dragged
            return
        elif event.type in key_backspace:
            self.input_text = self.input_text[:-1]
            self.offset = fn.try_str_to_float(self.input_text)
            self.input_text_last = self.input_text
            self.if_multi_dragged_stop(context, event) # remesh, update line
            return
        elif event.type in key_orientation:
            self.def_multi_swap_orientation()
            self.def_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_factor_mode:
            self.def_mode = self.if_mode_multi_fac
            self.def_multi_drag = self.if_multi_fac_drag_stop
            self.def_dragged = self.if_multi_fac_dragged_stop
            self.factor = fn.try_str_to_float(self.input_text)
            self.line[1][1] = fn.format_str(self.input_text)
            self.line[0][1] = "           N/A"
            
            self.line_color[0][0] = self.P.color_title_dark
            self.line_color[0][1] = self.P.color_num_dark
            self.line_color[1][0] = self.P.color_title
            self.line_color[1][1] = self.P.color_num
            self.rec_color_offset = self.P.color_block_2
            self.rec_color_length = self.P.color_block_input
            self.line[2][2] = "Factor mode"
            self.multi_fac_remesh()
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
            self.if_multi_dragged_stop(context, event) # remesh, update line


    def if_remesh_local(self):
        for i in range(0, self.len_el):
            self.sel_vert_el[i].co = self.org_el[i].co + (
                self.direction_nor[i] *self.offset)
    def if_remesh_unlocal(self):
        for i in range(0, self.len_el):
            self.sel_vert_el[i].co = self.org_el[i].co + (
                self.direction_nor_world[i] *self.offset)
        

    def if_multi_swap_orientation_local(self):
        self.def_multi_swap_orientation = self.if_multi_swap_orientation_unlocal
        self.def_remesh = self.if_remesh_unlocal
        self.line[4][1] = "Global"
    def if_multi_swap_orientation_unlocal(self):
        self.def_multi_swap_orientation = self.if_multi_swap_orientation_local
        self.def_remesh = self.if_remesh_local
        self.line[4][1] = "Local"

# //////////////////////////////////////////////////////////////////////////////
# ▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_mode_multi_fac(self, context, event):
        self.def_multi_drag(context, event)
# __  ________________________________________________________________
# ▇__▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_multi_fac_drag_do(self, context, event):
        self.get_key_inMultiFacDrag(context, event)
        # if mouse move: to self.offset, line , remesh (if need)
        self.def_dragged(context, event)
    def if_multi_fac_drag_stop(self, context, event):
        self.get_key_inMultiFacDirect(context, event)
# __  __  ____________________________________________________________
# ▇__▇__▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_multi_fac_dragged(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = event.mouse_x - self.mouse_x_last
            if math.fabs(delta) < self.win_width_half:
                self.mouse_x_offset += delta
                self.factor = round(self.mouse_x_offset *self.sensitive_fac, 3)
                self.line[1][1] = fn.format_f(self.factor)
                self.multi_fac_remesh()
                bmesh.update_edit_mesh(self.obj.data, True)
            self.loop_mouse(context, event)
    def if_multi_fac_dragged_stop(self, context, event):
        self.line[1][1] = fn.format_str(self.input_text)
        self.multi_fac_remesh()
        bmesh.update_edit_mesh(self.obj.data, True)
# __  __  __  ________________________________________________________

    def get_key_inMultiFacDrag(self, context, event):
        if event.value != 'PRESS':
            return

        if event.type in key_confirm:
            self.def_modal = self.if_modal_fin
            return
        elif event.type in key_cancel:
            self.def_modal = self.if_modal_cancel
            return
        elif event.type in key_0:
            self.factor = 0.0
            self.input_text = "0"
        elif event.type in key_1:
            self.factor = 1.0
            self.input_text = "1"
        elif event.type in key_2:
            self.factor = 2.0
            self.input_text = "2"
        elif event.type in key_3:
            self.factor = 3.0
            self.input_text = "3"
        elif event.type in key_4:
            self.factor = 4.0
            self.input_text = "4"
        elif event.type in key_5:
            self.factor = 5.0
            self.input_text = "5"
        elif event.type in key_6:
            self.factor = 6.0
            self.input_text = "6"
        elif event.type in key_7:
            self.factor = 7.0
            self.input_text = "7"
        elif event.type in key_8:
            self.factor = 8.0
            self.input_text = "8"
        elif event.type in key_9:
            self.factor = 9.0
            self.input_text = "9"
        elif event.type in key_dot:
            self.factor = 0.0
            self.input_text = "0."
        elif event.type in key_minus:
            self.factor = 0.0
            self.input_text = "-"
        elif event.type in key_reset:
            self.factor = 1.0
            self.line[1][1] = fn.format_str("1")
            self.mouse_x_offset = int(1 / self.sensitive_fac)
            self.multi_fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_backspace:
            self.input_text = fn.str_f(self.factor)
            self.input_text = self.input_text[:-1]
            self.factor = fn.try_str_to_float(self.input_text)
        elif event.type in key_orientation:
            self.def_multi_swap_orientation()
            context.area.tag_redraw()
            return
        elif event.type in key_factor_mode:
            self.def_mode = self.if_mode_multi
            self.def_multi_drag = self.if_multi_drag_do
            self.def_dragged = self.if_multi_dragged
            self.offset = round(self.mouse_x_offset * self.sensitive_fac, 3)
            self.mouse_x_offset = self.offset / self.sensitive
            self.line[0][1] = fn.format_f(self.offset)
            self.line[1][1] = "           N/A"
            
            self.line_color[0][0] = self.P.color_title
            self.line_color[0][1] = self.P.color_num
            self.line_color[1][0] = self.P.color_title_dark
            self.line_color[1][1] = self.P.color_num_dark
            self.rec_color_offset = self.P.color_block
            self.rec_color_length = self.P.color_block_2
            self.line[2][2] = ""
            self.def_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        else:
            return
        # press [0123456789.-][backspace]: through here
        self.input_text_last = self.input_text
        self.def_multi_drag = self.if_multi_fac_drag_stop
        self.def_dragged = self.if_multi_fac_dragged_stop
        context.window.cursor_set('CROSSHAIR')
        self.rec_color_length = self.P.color_block_input

    def get_key_inMultiFacDirect(self, context, event):
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
        elif event.type in key_reset:
            context.window.cursor_set('SCROLL_X')
            self.factor = 1.0
            self.line[1][1] = fn.format_str("1")
            self.mouse_x_offset = int(1 / self.sensitive_fac)
            self.mouse_x_last = event.mouse_x
            self.rec_color_length = self.P.color_block
            self.multi_fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            self.def_multi_drag = self.if_multi_fac_drag_do
            self.def_dragged = self.if_multi_fac_dragged
            return
        elif event.type in key_backspace:
            self.input_text = self.input_text[:-1]
            self.factor = fn.try_str_to_float(self.input_text)
            self.input_text_last = self.input_text
            self.if_multi_fac_dragged_stop(context, event) # remesh, update line
            return
        elif event.type in key_orientation:
            self.def_multi_swap_orientation()
            context.area.tag_redraw()
            return
        elif event.type in key_factor_mode:
            self.def_mode = self.if_mode_multi
            self.def_multi_drag = self.if_multi_drag_stop
            self.def_dragged = self.if_multi_dragged_stop
            self.offset = fn.try_str_to_float(self.input_text)
            self.line[0][1] = fn.format_str(self.input_text)
            self.line[1][1] = "           N/A"

            self.line_color[0][0] = self.P.color_title
            self.line_color[0][1] = self.P.color_num
            self.line_color[1][0] = self.P.color_title_dark
            self.line_color[1][1] = self.P.color_num_dark
            self.rec_color_offset = self.P.color_block_input
            self.rec_color_length = self.P.color_block_2
            self.line[2][2] = ""
            self.def_remesh()
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
            self.factor = try_to_float
            self.if_multi_fac_dragged_stop(context, event) # remesh, update line

    def multi_fac_remesh(self):
        self.multi_factor = self.factor - 1
        for i in range(0, self.len_el):
            self.sel_vert_el[i].co = self.org_el[i].co + (
                self.direction[i] *self.multi_factor)