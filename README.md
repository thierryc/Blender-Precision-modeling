# Precision Modeling Switch

Precision Modeling Switch is a small Blender add-on that toggles a scene and all open 3D viewports between Blender's default modeling setup and a **millimeter-accurate configuration** suitable for **3D printing** or building **small industrial design objects**.


## Features
- Switch between **Default** and **Precision** modes
- Precision mode uses metric units in millimeters, enables snapping, adjusts grid and clip range
- Default mode restores Blender-like settings
- Optional *Save as Startup* button to keep the current mode as the default

## Installation

Recommended (from Releases):
- Download the latest `precision-modeling-switch-<tag>.zip` from the GitHub **Releases** page.
- Do not unzip. In Blender open **Edit → Preferences → Add-ons → Install…** and choose the ZIP. Enable
  the add-on entry named "Precision Modeling Switch".

If your browser auto-unzips (e.g., Safari):
- Option A: Disable auto-unzip in Safari (Preferences → General → uncheck "Open ‘safe’ files after downloading"). Re‑download.
- Option B: Re‑zip the folder you got and install that ZIP:
  - macOS: Finder → right‑click the folder → **Compress "precision_modeling_switch"** → install the resulting `.zip`.
  - Windows: Explorer → right‑click the folder → **Send to → Compressed (zipped) folder**.
  - Linux: In a terminal: `zip -r precision-modeling-switch.zip precision_modeling_switch/`.

Manual install (if building locally):
- Create a folder named `precision_modeling_switch` containing the repository’s `__init__.py` (and optional `README.md`, `LICENSE`). Zip that folder and install it via **Add-ons → Install…** as above.

## Usage
Open the *N* sidebar in the 3D Viewport and select the **Precision** panel.  
Use **Default** or **Precision** to apply settings to the active scene and all open viewports.  
Press **Save as Startup** to store the current configuration as your Blender default.

## License
This project is released under the [GPL-3.0-or-later](LICENSE) license.

<img width="1840" height="1191" alt="image" src="https://github.com/user-attachments/assets/31c0b26c-6d7a-4984-9f8f-9199d417247b" />

## Release Notes

### 1.0.0
- Fix: Prevent temporary jaggy/blurry artifacts in the viewport when switching to Precision mode by applying settings step‑by‑step and using a safer near clip value (1 mm) to avoid depth precision issues.
- Add: Clear installation instructions and packaged release ZIP for easy install.
