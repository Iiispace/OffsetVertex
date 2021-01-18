import math, bmesh
import numpy as np

class fn():
    small_num = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "⁻"]

    @staticmethod
    def format_f(f):
        s = format(f, 'f')
        
        output = ""
        ind_dot = s.find(".")

        while True:
            if s[-1] == '0':
                s = s[:-1]
            else:
                break
        
        ind = 7 - ind_dot
        i = 0
        while ind > 0:
            output += " "
            ind -= 1
            if i % 3 == 0:
                output += " "
            i += 1

        ind = 1
        if s[0] == '-':
            if i % 3 == 0:
                output += " -"
            else:
                output += "-"
        else:
            output += s[0]
            if i % 3 == 0:
                if s[1] != '.':
                    output += " "
        i += 1

        while ind < ind_dot - 1:
            output += s[ind]
            ind += 1
            if i % 3 == 0:
                output += " "
            i += 1

        if ind < ind_dot:
            output += s[ind]

        if s[-1] == '.':
            return output
        
        output += s[ind_dot]
        ind_dot += 1
        ind = len(s) - ind_dot
        i = 1
        while True:
            output += s[ind_dot]
            ind_dot += 1
            ind -= 1
            if ind < 1:
                break
            if i % 3 == 0:
                output += " "
            i += 1
        
        return output

    @staticmethod
    def format_f_degree(f):
        s = format(f, '.5f')
        
        output = ""
        ind_dot = s.find(".")

        while True:
            if s[-1] == '0':
                s = s[:-1]
            else:
                break
        
        ind = 7 - ind_dot
        i = 0
        while ind > 0:
            output += " "
            ind -= 1
            if i % 3 == 0:
                output += " "
            i += 1

        ind = 1
        if s[0] == '-':
            if i % 3 == 0:
                output += " -"
            else:
                output += "-"
        else:
            output += s[0]
            if i % 3 == 0:
                if s[1] != '.':
                    output += " "
        i += 1

        while ind < ind_dot - 1:
            output += s[ind]
            ind += 1
            if i % 3 == 0:
                output += " "
            i += 1

        if ind < ind_dot:
            output += s[ind]

        if s[-1] == '.':
            return output + "°"
        
        output += s[ind_dot]
        ind_dot += 1
        ind = len(s) - ind_dot
        i = 1
        while True:
            output += s[ind_dot]
            ind_dot += 1
            ind -= 1
            if ind < 1:
                break
            if i % 3 == 0:
                output += " "
            i += 1
        
        return output + "°"

    @staticmethod
    def format_f_sci(f, c):
        s = format(f, c)
        output = ""
        ind_e = s.find("e")

        output = s[0:ind_e]
        output += " x 10"
        i = ind_e + 1
        if s[i] == "-":
            output += "⁻"
        i += 1
        first = True
        while i < len(s):
            if first:
                if s[i] != "0":
                    output += fn.small_num[int(s[i])]
                    first = False
                elif s[i+1] == "0":
                    output += fn.small_num[0]
                    return output
            else:
                output += fn.small_num[int(s[i])]
            i += 1
        return output

    @staticmethod
    def format_str(s):        
        output = ""
        ind_dot = s.find(".")
        len_s = len(s)

        if len_s == 0:
            return output
        
        no_dot = False
        if ind_dot == -1:
            ind_dot = len(s)
            no_dot = True
        
        ind = 7 - ind_dot
        i = 0
        while ind > 0:
            output += " "
            ind -= 1
            if i % 3 == 0:
                output += " "
            i += 1

        if len_s == 1:
            output += s[0]
            return output

        ind = 1
        if s[0] == '-':
            if i % 3 == 0:
                output += " -"
            else:
                output += "-"
        else:
            output += s[0]
            if i % 3 == 0:
                if s[1] != '.':
                    output += " "
        i += 1

        while ind < ind_dot - 1:
            output += s[ind]
            ind += 1
            if i % 3 == 0:
                output += " "
            i += 1

        if ind < ind_dot:
            output += s[ind]

        if s[-1] == '.':
            output += "."
            return output

        if no_dot:
            return output
        
        output += s[ind_dot]
        ind_dot += 1
        ind = len(s) - ind_dot
        i = 1
        while True:
            output += s[ind_dot]
            ind_dot += 1
            ind -= 1
            if ind < 1:
                break
            if i % 3 == 0:
                output += " "
            i += 1
        
        return output

    @staticmethod
    def str_f(f):
        output = str(f)
        while output[-1:] == "0":
            output = output[:-1]
        
        if output[-1:] == ".":
            output = output[:-1]
        return output

    @staticmethod
    def get_active_vertex_elem(bm):
        try:
            for elem in reversed(bm.select_history):
                if isinstance(elem, bmesh.types.BMVert):
                    return elem
        except:
            return None

    # @staticmethod
    # def get_active_edge_elem(bm):
    #     try:
    #         for elem in reversed(bm.select_history):
    #             if isinstance(elem, bmesh.types.BMEdge):
    #                 return elem
    #     except:
    #         return None

    # @staticmethod
    # def get_active_face_elem(bm):
    #     try:
    #         for elem in reversed(bm.select_history):
    #             if isinstance(elem, bmesh.types.BMFace):
    #                 return elem
    #     except:
    #         return None

    @staticmethod
    def get_selected_vert(bm):
        vert = []

        for v in bm.verts:
            if (v.select == True):
                vert.append(v)
        return vert


    @staticmethod
    def get_areas_by_type(context, type):
        return [a for a in context.screen.areas if a.type == type]

    @staticmethod
    def unit_vector(vector):
        return vector / np.linalg.norm(vector)

    @staticmethod
    def angle_between(v1, v2):
        v1_u = fn.unit_vector(v1)
        v2_u = fn.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    @staticmethod
    def get_user_prefs(context):
        if hasattr(context, "user_preferences"):
            return context.user_preferences

        return context.preferences

    @staticmethod
    def try_str_to_float(s):
        if s in {"", "-"}:
            return 0.0
        
        try:
            f = float(s)
            return f
        except:
            return None

