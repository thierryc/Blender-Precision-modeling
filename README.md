# Precision Modeling Switch

Precision Modeling Switch is a small Blender add-on that toggles a scene and all open 3D viewports between Blender's default modeling setup and a millimeter-accurate configuration suitable for 3D printing.

## Features
- Switch between **Default** and **Precision** modes
- Precision mode uses metric units in millimeters, enables snapping, adjusts grid and clip range
- Default mode restores Blender-like settings
- Optional *Save as Startup* button to keep the current mode as the default

## Installation
1. Download or clone this repository
2. Zip the add-on folder (containing `__init__.py`)
3. In Blender, open **Edit → Preferences → Add-ons**
4. Click **Install…**, select the ZIP file, then enable *Precision Modeling Switch*

## Usage
Open the *N* sidebar in the 3D Viewport and select the **Precision** panel.  
Use **Default** or **Precision** to apply settings to the active scene and all open viewports.  
Press **Save as Startup** to store the current configuration as your Blender default.

## License
This project is released under the [GPL-3.0-or-later](LICENSE) license.
