from .op_factor import *

class OffsetVert_Length(OffsetVert_Factor):
    bl_idname = "object.offset_vert_operator"
    bl_label = "Offset Vertex Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):        
        super().__init__()

        self.def_length_drag = self.if_length_drag_do

# ▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_mode_length(self, context, event):
        self.def_length_drag(context, event)
# __  ________________________________________________________________
# ▇__▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_length_drag_do(self, context, event):
        self.get_key_inLenDrag(context, event)
        # if mouse move: to self.lenegth, line , remesh (if need)
        self.def_dragged(context, event)
    def if_length_drag_stop(self, context, event):
        self.get_key_inLenDirect(context, event)
# __  __  ____________________________________________________________
# ▇__▇__▇__▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇
    def if_length_dragged(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = event.mouse_x - self.mouse_x_last
            if math.fabs(delta) < self.win_width_half:
                self.mouse_x_offset += delta
                self.length = round(self.mouse_x_offset *self.sensitive, 3)
                self.line[1][1] = fn.format_f(self.length)
                self.factor = self.def_return_factor_from_length()
                self.line[2][1] = fn.format_f(self.factor)
                self.line[0][1] = fn.format_f(self.def_return_offset_from_factor())
                self.fac_remesh()
                bmesh.update_edit_mesh(self.obj.data, True)
            self.loop_mouse(context, event)
    def if_length_dragged_stop(self, context, event):
        self.line[1][1] = fn.format_str(self.input_text)
        self.factor = self.def_return_factor_from_length()
        self.line[2][1] = fn.format_f(self.factor)
        self.line[0][1] = fn.format_f(self.def_return_offset_from_factor())
        self.fac_remesh()
        bmesh.update_edit_mesh(self.obj.data, True)
# __  __  __  ________________________________________________________


    def get_key_inLenDrag(self, context, event):
        if event.value != 'PRESS':
            return

        if event.type in key_confirm:
            self.def_modal = self.if_modal_fin
            return
        elif event.type in key_cancel:
            self.def_modal = self.if_modal_cancel
            return
        elif event.type in key_0:
            self.length = 0.0
            self.input_text = "0"
        elif event.type in key_1:
            self.length = 1.0
            self.input_text = "1"
        elif event.type in key_2:
            self.length = 2.0
            self.input_text = "2"
        elif event.type in key_3:
            self.length = 3.0
            self.input_text = "3"
        elif event.type in key_4:
            self.length = 4.0
            self.input_text = "4"
        elif event.type in key_5:
            self.length = 5.0
            self.input_text = "5"
        elif event.type in key_6:
            self.length = 6.0
            self.input_text = "6"
        elif event.type in key_7:
            self.length = 7.0
            self.input_text = "7"
        elif event.type in key_8:
            self.length = 8.0
            self.input_text = "8"
        elif event.type in key_9:
            self.length = 9.0
            self.input_text = "9"
        elif event.type in key_dot:
            self.length = 0.0
            self.input_text = "0."
        elif event.type in key_minus:
            self.length = 0.0
            self.input_text = "-"
        elif event.type in key_flip:
            self.flip_vert()
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_reset:
            self.offset = 0.0
            self.factor = 1.0
            self.length = self.def_return_length_from_offset()
            self.mouse_x_offset = self.length / self.sensitive
            self.line[0][1] = fn.format_str("0")
            self.line[1][1] = fn.format_f(self.length)
            self.line[2][1] = fn.format_str("1")
            self.reset_vert()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_backspace:
            self.input_text = fn.str_f(self.length)
            self.input_text = self.input_text[:-1]
            self.length = fn.try_str_to_float(self.input_text)
        elif event.type in key_orientation:
            self.def_swap_orientation()
            self.factor = self.def_return_factor_from_length()
            self.line[2][1] = fn.format_f(self.factor)
            self.line[0][1] = fn.format_f(self.def_return_offset_from_factor())
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_length_mode:
            self.def_mode = self.if_mode_offset
            self.def_drag = self.if_drag_do
            self.def_dragged = self.if_dragged
            self.offset = round(self.mouse_x_offset * self.sensitive, 3)
            self.mouse_x_offset = self.offset / self.sensitive
            self.line[0][1] = fn.format_f(self.offset)
            self.length = self.def_return_length_from_offset()
            self.line[1][1] = fn.format_f(self.length)
            self.factor = self.def_return_factor_from_length()
            self.line[2][1] = fn.format_f(self.factor)

            self.line_color[0][0] = self.P.color_title
            self.line_color[0][1] = self.P.color_num
            self.line_color[1][0] = self.P.color_title_dark
            self.line_color[1][1] = self.P.color_num_dark
            self.rec_color_offset = self.P.color_block
            self.rec_color_length = self.P.color_block_2
            self.line[3][2] = ""
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

            self.line_color[1][0] = self.P.color_title_dark
            self.line_color[1][1] = self.P.color_num_dark
            self.line_color[2][0] = self.P.color_title
            self.line_color[2][1] = self.P.color_num
            self.rec_color_length = self.P.color_block_2
            self.rec_color_factor = self.P.color_block
            self.line[3][2] = "Factor mode"
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        else:
            return
        # press [0123456789.-][backspace]: through here
        self.input_text_last = self.input_text
        self.def_length_drag = self.if_length_drag_stop
        self.def_dragged = self.if_length_dragged_stop
        context.window.cursor_set('CROSSHAIR')
        self.rec_color_length = self.P.color_block_input

    def get_key_inLenDirect(self, context, event):
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
            self.length = self.def_return_length_from_offset()
            self.mouse_x_offset = self.length / self.sensitive
            self.mouse_x_last = event.mouse_x
            self.line[0][1] = fn.format_str("0")
            self.line[1][1] = fn.format_f(self.length)
            self.line[2][1] = fn.format_str("1")
            self.rec_color_length = self.P.color_block
            self.reset_vert()
            bmesh.update_edit_mesh(self.obj.data, True)
            self.def_length_drag = self.if_length_drag_do
            self.def_dragged = self.if_length_dragged
            return
        elif event.type in key_backspace:
            self.input_text = self.input_text[:-1]
            self.length = fn.try_str_to_float(self.input_text)
            self.input_text_last = self.input_text
            self.if_length_dragged_stop(context, event) # remesh, update line
            return
        elif event.type in key_orientation:
            self.def_swap_orientation()
            self.factor = self.def_return_factor_from_length()
            self.line[2][1] = fn.format_f(self.factor)
            self.line[0][1] = fn.format_f(self.def_return_offset_from_factor())
            self.fac_remesh()
            bmesh.update_edit_mesh(self.obj.data, True)
            return
        elif event.type in key_length_mode:
            self.def_mode = self.if_mode_offset
            self.def_drag = self.if_drag_stop
            self.def_dragged = self.if_dragged_stop
            self.offset = fn.try_str_to_float(self.input_text)
            self.line[0][1] = fn.format_str(self.input_text)
            self.length = self.def_return_length_from_offset()
            self.line[1][1] = fn.format_f(self.length)
            self.factor = self.def_return_factor_from_length()
            self.line[2][1] = fn.format_f(self.factor)

            self.line_color[0][0] = self.P.color_title
            self.line_color[0][1] = self.P.color_num
            self.line_color[1][0] = self.P.color_title_dark
            self.line_color[1][1] = self.P.color_num_dark
            self.rec_color_offset = self.P.color_block_input
            self.rec_color_length = self.P.color_block_2
            self.line[3][2] = ""
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

            self.line_color[1][0] = self.P.color_title_dark
            self.line_color[1][1] = self.P.color_num_dark
            self.line_color[2][0] = self.P.color_title
            self.line_color[2][1] = self.P.color_num
            self.rec_color_length = self.P.color_block_2
            self.rec_color_factor = self.P.color_block_input
            self.line[3][2] = "Factor mode"
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
            self.length = try_to_float
            self.if_length_dragged_stop(context, event) # remesh, update line

    def if_return_offset_local(self):
        return self.length - self.direction_length
    def if_return_offset_unlocal(self):
        return self.length - self.direction_world_length