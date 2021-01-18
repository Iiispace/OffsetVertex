from .op_multi import *

class OffsetVert_Operator(OffsetVert_Multi):
    bl_idname = "object.offset_vert_operator"
    bl_label = "Offset Vertex Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):        
        super().__init__()