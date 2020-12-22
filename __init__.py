import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ExportHelper, ImportHelper
from re import compile

bl_info = {
    'name': 'Sequence .dat poses',
    'author': 'gabriel montagné, gabriel@tibas.london',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'description': "Applies .dat pose library names to selected bones",
    'category': 'Animation'
}

dat_line = compile(r'^(\d+) (.*)')

class ANIMATION_OT_sequence_dat_poses(Operator, ImportHelper):
    """Sequence poses from .dat animation file"""
    bl_idname = "animation.dat_sequence_animation"
    bl_label = "Sequence poess from .dat animation file"

    filename_ext = ".dat"
    filter_glob: StringProperty(default="*.dat", options={'HIDDEN'}, maxlen=255)

    @classmethod
    def poll(cls, context):
        a = context.active_object
        return a and a.type == 'ARMATURE' and a.pose_library

    def execute(self, context):
        scene = context.scene
        lib = context.active_object.pose_library
        markers = lib.pose_markers

        with open(self.properties.filepath, 'r') as f:
            not_found = set()
            for line in f:
                m = dat_line.fullmatch(line.strip())
                if not m: continue
                f, t = m.groups()
                i = markers.find(t)
                if i == -1:
                    not_found.add(t)
                    continue

                p = markers.get(t)
                print('yvar', i, f, t, p)

                context.scene.frame_current = int(f)
                bpy.ops.poselib.apply_pose(pose_index=i)

            if not_found:
                self.report({'WARNING'}, "Couldn't find {} poses".format(not_found))

        return {'FINISHED'}

def register():
    print('Registering Seqnce DAT poses')
    register_class(ANIMATION_OT_sequence_dat_poses)

def unregister():
    print('Registering Seqnce DAT poses')
    unregister_class(ANIMATION_OT_sequence_dat_poses)
