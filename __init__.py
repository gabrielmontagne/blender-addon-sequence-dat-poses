from bpy import ops
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ExportHelper, ImportHelper
from re import compile

bl_info = {
    'name': 'Sequence .dat poses',
    'author': 'gabriel montagné, gabriel@tibas.london',
    'version': (0, 0, 3),
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
    filter_glob: StringProperty(
        default="*.dat", options={'HIDDEN'}, maxlen=255)
    add_timeline_markers: BoolProperty(default=False)
    offset_to_current_frame: BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        a = context.active_object
        return a and a.type == 'ARMATURE' and hasattr(a, 'pose_library') and a.pose_library

    def execute(self, context):
        scene = context.scene
        insert_auto = scene.tool_settings.use_keyframe_insert_auto
        frame_current = scene.frame_current

        lib = context.active_object.pose_library
        markers = lib.pose_markers
        scene.tool_settings.use_keyframe_insert_auto = True

        frame_offset = 0

        if self.offset_to_current_frame:
            frame_offset = frame_current 

        with open(self.properties.filepath, 'r') as f:
            not_found = set()
            for line in f:
                m = dat_line.fullmatch(line.strip())
                if not m:
                    continue
                f, t = m.groups()
                i = markers.find(t)
                if i == -1:
                    not_found.add(t)
                    continue

                p = markers.get(t)
                frame = int(f)
                context.scene.frame_current = frame + frame_offset
                ops.poselib.apply_pose(pose_index=i)

                if self.add_timeline_markers:
                    scene.timeline_markers.new(t, frame=frame)

            if not_found:
                self.report(
                    {'WARNING'}, "Couldn't find {} poses".format(not_found))

        scene.tool_settings.use_keyframe_insert_auto = insert_auto
        scene.frame_current = frame_current
        return {'FINISHED'}


def register():
    register_class(ANIMATION_OT_sequence_dat_poses)


def unregister():
    unregister_class(ANIMATION_OT_sequence_dat_poses)
