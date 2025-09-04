# SPDX-License-Identifier: GPL-3.0-or-later

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

def iter_view3d_areas_spaces():
    """Yield (area, space) for all View3D spaces across all windows."""
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        yield area, space


def redraw_all_viewports():
    """Request a redraw on all areas and flush once if possible."""
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            area.tag_redraw()
    try:
        bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)
    except Exception:
        # The operator may fail in some contexts; tagging is enough.
        pass


def apply_precision(context):
    """Configure scene and viewports for millimeter precision.

    Applies settings in small, explicit steps with redraws to
    avoid transient GL artifacts. Also keeps a safer near clip
    to prevent depth-buffer z-fighting.
    """
    scene = context.scene
    units = scene.unit_settings

    # Units (step-by-step) -------------------------------------------------
    units.system = "METRIC"
    redraw_all_viewports()
    units.length_unit = "MILLIMETERS"
    redraw_all_viewports()
    units.scale_length = 0.001
    redraw_all_viewports()

    # Snapping (step-by-step) ----------------------------------------------
    ts = scene.tool_settings
    ts.use_snap = True
    redraw_all_viewports()
    ts.snap_elements = {"INCREMENT"}
    redraw_all_viewports()
    ts.use_snap_grid_absolute = True
    redraw_all_viewports()
    ts.use_snap_translate = True
    redraw_all_viewports()
    ts.use_snap_rotate = True
    redraw_all_viewports()
    ts.use_snap_scale = True
    redraw_all_viewports()

    # Viewports -------------------------------------------------------------
    # Use 1 mm as near clip to greatly reduce z-fighting in Solid mode.
    safe_near_clip = 0.001

    for area, space in iter_view3d_areas_spaces():
        overlay = space.overlay
        overlay.grid_scale = 0.001
        area.tag_redraw()
        overlay.grid_subdivisions = 10
        area.tag_redraw()
        space.clip_start = safe_near_clip
        area.tag_redraw()

    redraw_all_viewports()


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

    for area, space in iter_view3d_areas_spaces():
        overlay = space.overlay
        overlay.grid_scale = 1.0
        area.tag_redraw()
        overlay.grid_subdivisions = 10
        area.tag_redraw()
        space.clip_start = 0.01
        area.tag_redraw()

    redraw_all_viewports()


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
