# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Precision Modeling Switch add-on."""

from __future__ import annotations

import bpy


bl_info = {
    "name": "Precision Modeling Switch",
    "author": "Thierry Charbonnel",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Precision",
    "description": "Toggle precision settings for modeling in millimeters.",
    "category": "3D View",
    "support": "COMMUNITY",
    "doc_url": "https://example.com/docs",
    "tracker_url": "https://example.com/issues",
}


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def iter_view3d_spaces():
    """Yield all View3D spaces across all open windows."""
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        yield space


def apply_precision(context):
    """Configure scene and viewports for millimeter precision."""
    scene = context.scene
    units = scene.unit_settings
    units.system = "METRIC"
    units.length_unit = "MILLIMETERS"
    units.scale_length = 0.001

    ts = scene.tool_settings
    ts.use_snap = True
    ts.snap_elements = {"INCREMENT"}
    ts.use_snap_grid_absolute = True
    ts.use_snap_translate = True
    ts.use_snap_rotate = True
    ts.use_snap_scale = True

    for space in iter_view3d_spaces():
        overlay = space.overlay
        overlay.grid_scale = 0.001
        overlay.grid_subdivisions = 0
        space.clip_start = 0.0001


def apply_default(context):
    """Restore Blender's default scene and viewport settings."""
    scene = context.scene
    units = scene.unit_settings
    units.system = "METRIC"
    units.length_unit = "METERS"
    units.scale_length = 1.0

    ts = scene.tool_settings
    ts.use_snap = False
    ts.snap_elements = {"INCREMENT"}
    ts.use_snap_grid_absolute = False
    ts.use_snap_translate = False
    ts.use_snap_rotate = False
    ts.use_snap_scale = False

    for space in iter_view3d_spaces():
        overlay = space.overlay
        overlay.grid_scale = 1.0
        overlay.grid_subdivisions = 10
        space.clip_start = 0.01


# -----------------------------------------------------------------------------
# Operators
# -----------------------------------------------------------------------------


class PM_OT_apply_precision(bpy.types.Operator):
    """Enable precision setup for 3D printing."""

    bl_idname = "pm.apply_precision"
    bl_label = "Precision Mode"

    def execute(self, context):
        apply_precision(context)
        return {"FINISHED"}


class PM_OT_apply_default(bpy.types.Operator):
    """Restore Blender-like defaults."""

    bl_idname = "pm.apply_default"
    bl_label = "Default Mode"

    def execute(self, context):
        apply_default(context)
        return {"FINISHED"}


# -----------------------------------------------------------------------------
# UI Panel
# -----------------------------------------------------------------------------


class PM_PT_panel(bpy.types.Panel):
    bl_label = "Precision"
    bl_idname = "PM_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Precision"

    def draw(self, context):
        layout = self.layout
        layout.operator("pm.apply_default", text="Default")
        layout.operator("pm.apply_precision", text="Precision")
        layout.operator("wm.save_homefile", text="Save as Startup", icon="FILE_TICK")


# -----------------------------------------------------------------------------
# Registration
# -----------------------------------------------------------------------------

classes = (
    PM_OT_apply_default,
    PM_OT_apply_precision,
    PM_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
