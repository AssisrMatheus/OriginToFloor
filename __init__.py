bl_info = {
    "name": "Origin to Floor",
    'author': 'AssisrMatheus',
    'version': (1, 0, 0),
    'blender': (2, 80, 0),
    'location': 'Object > Origin to Floor',
    'description': 'Centers the origin on the floor of the selected object',
    "category": "Object",
    "tracker_url": "https://github.com/AssisrMatheus/OriginToFloor/issues",
    "wiki_url": "https://github.com/AssisrMatheus/OriginToFloor",
}

import bpy

def set_origin_to_floor(shouldClear):
    # Get the selected object
    obj = bpy.context.active_object

    # Stores the current edit mode so we can rollback later
    current_mode = obj.mode

    # The method used to get the vertices depends on being on object mode
    bpy.ops.object.mode_set(mode = 'OBJECT')

    # Stores the current pivot point transform setting
    current_pivot = bpy.context.scene.tool_settings.transform_pivot_point

    # Sets the pivot point transform setting so the origin calculation is exactly at the center
    bpy.context.scene.tool_settings.transform_pivot_point = "BOUNDING_BOX_CENTER"

    # Puts the origin in the center of the object
    bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')

    # Resets back to the previous pivot point transform setting
    bpy.context.scene.tool_settings.transform_pivot_point = current_pivot

    # Grabs all the vertices, then their coordinates, then their Z position
    z_verts = [v.co.z for v in obj.data.vertices]

    # Grabs the most negative Z position(floor position)
    deepest_vert_z = min(z_verts)

    # We're going to translate only the origin for now
    bpy.context.scene.tool_settings.use_transform_data_origin = True

    # Translate the origin only on Z, to the same position as vertex that is closest to the bottom
    bpy.ops.transform.translate(value=(0, 0, deepest_vert_z))

    # Reset the origin manipulation back
    bpy.context.scene.tool_settings.use_transform_data_origin = False

    if shouldClear:
        bpy.ops.object.location_clear(clear_delta=False)

    # Resets the object mode back to what it was previously
    bpy.ops.object.mode_set(mode = current_mode)

class OriginToFloor(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.origin_to_floor"
    bl_label = "Origin to Floor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        # Only if there's a selected object
        return obj is not None

    def execute(self, context):
        set_origin_to_floor(False)
        return {'FINISHED'}

class OriginToFloorClear(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.origin_to_floor_clear"
    bl_label = "Origin to Floor(Clear position)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        # Only if there's a selected object
        return obj is not None

    def execute(self, context):
        set_origin_to_floor(True)
        return {'FINISHED'}

def menu_func(self, context):
    layout = self.layout
    layout.operator(OriginToFloor.bl_idname)
    layout.operator(OriginToFloorClear.bl_idname)

def register():
    bpy.utils.register_class(OriginToFloor)
    bpy.utils.register_class(OriginToFloorClear)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OriginToFloor)
    bpy.utils.unregister_class(OriginToFloorClear)

if __name__ == "__main__":
    register()
