# BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# END GPL LICENSE BLOCK #####

bl_info = {
    "name" : "Iiispace - Offset Vertex",
    "author" : "Iiispace",
    "version" : (1, 0),
    "blender" : (2, 80, 0),
    "location" : "View3d > Tool",
    "warning" : "",
    "description" : "",
    "wiki_url" : "",
    "category" : "Mesh",
}

import bpy
from bpy.utils import register_class, unregister_class

from .import op
from .import preferences
from .import ui

classes = (
    op.OffsetVert_Operator,
    preferences.OffsetVert_Preferences,
    ui.OffsetVert_Panel,
)

addon_keymaps = []
def register():
    for c in classes:
        register_class(c)
    
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("object.offset_vert_operator", type= 'ONE', value= 'PRESS', shift= False)
        addon_keymaps.append((km, kmi))

def unregister():
    for c in classes:
        unregister_class(c)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
