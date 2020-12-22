from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper, ImportHelper
from bpy.utils import register_class, unregister_class
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

    def execute(self, context):
        scene = context.scene

        with open(self.properties.filepath, 'r') as f:
            for line in f:
                m = dat_line.fullmatch(line.strip())
                if not m: continue
                i, t = m.groups()
                print('yvar', i, t)

        return {'FINISHED'}

def register():
    print('Registering Seqnce DAT poses')
    register_class(ANIMATION_OT_sequence_dat_poses)

def unregister():
    print('Registering Seqnce DAT poses')
    unregister_class(ANIMATION_OT_sequence_dat_poses)
