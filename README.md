# StreetView Pro

Open Google Street View directly from the QGIS map canvas with an animated hanging Pegman cursor, customizable heading, and smart right-click tools.

![QGIS Version](https://img.shields.io/badge/QGIS-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-2.0-orange.svg)

---

## Overview

StreetView Pro is a lightweight and interactive QGIS plugin that allows you to instantly open Google Street View from any map location.

With a smooth hanging Pegman cursor similar to Google Maps, you can click or drag to define the viewing direction, copy coordinates or Street View URLs, and seamlessly return to your workflow.

Designed for GIS professionals, photogrammetrists, surveyors, and map editors who need quick field verification and visual reference.

---

## Key Features (v2.0)

1. **Click or Drag to Open Street View**  
   Single click for instant view or drag to define custom heading.

2. **Directional Control with Visual Arrow**  
   A dynamic direction line with arrow shows the exact viewing angle.

3. **Animated Hanging Pegman Cursor**  
   Replaces the static camera icon with a Google-Maps-style Pegman.

4. **Dynamic Pegman Tilt Animation**  
   Pegman tilts left/right based on movement direction and speed.

5. **Right-Click Quick Access**  
   - Open Street View at clicked location  
   - Copy coordinates (X, Y format)  
   - Copy full Street View URL  

6. **Automatic Tool Reset**  
   Returns to the default selection tool after opening Street View.

7. **Full CRS Support**  
   Works with any project CRS and automatically transforms to WGS84.

8. **ESC Key Cancelation**  
   Cancel operation instantly without opening Street View.

9. **Dedicated StreetView Pro Toolbar**  
   Easy activation with clear message bar instructions.

---

## Installation

### From QGIS Plugin Repository (Recommended)

1. Open QGIS  
2. Go to `Plugins` → `Manage and Install Plugins`  
3. Search for **StreetView Pro**  
4. Click **Install Plugin**

---

### Manual Installation

1. Download the latest release from GitHub  
2. Extract the ZIP file  
3. Copy the `StreetView Pro` folder to:

**Windows**  
`C:\Users\YourUsername\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
or
`C:\Users\YourUsername\AppData\Roaming\QGIS\QGIS4\profiles\default\python\plugins\`

**macOS**  
`~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
or
`~/Library/Application Support/QGIS/QGIS4/profiles/default/python/plugins/`

**Linux**  
`~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
or
`~/.local/share/QGIS/QGIS4/profiles/default/python/plugins/`

4. Restart QGIS  
5. Enable the plugin from `Plugins` → `Manage and Install Plugins`

---

## Usage

### Basic Workflow

1. Click the **StreetView Pro** toolbar icon  
2. Move the hanging Pegman over the map  
3. **Single Click** → Opens Street View with default heading  
4. **Click & Drag** → Set custom viewing direction  
5. Release mouse → Street View opens in your default browser  

After opening, the plugin automatically switches back to the selection tool.

---

### Right-Click Options

Right-click anywhere on the map canvas to:

- Open Street View at that location  
- Copy coordinates (X, Y format)  
- Copy full Google Street View URL  

---

### Keyboard Shortcut

- **ESC** → Cancel and exit StreetView mode

---

## Technical Details

- **Plugin Name:** StreetView Pro  
- **Version:** 2.0  
- **Minimum QGIS Version:** 3.0  
- **Maximum QGIS Version:** 4.99  
- **Qt Compatibility:** Qt5 (QGIS 3) and Qt6 (QGIS 4)  
- **Category:** Web  
- **License:** MIT  
- **Language:** Python  

---

## How It Works

1. Captures click and drag events from the QGIS map canvas  
2. Calculates heading from drag direction  
3. Transforms coordinates from project CRS to WGS84  
4. Builds a Google Street View URL with heading parameters  
5. Opens the URL in the default web browser  

---

## Changelog

### Version 2.0 – Hanging Pegman Cursor Update

- Replaced static camera cursor with animated hanging Pegman  
- Added dynamic tilt animation based on movement  
- Improved visual interaction and user experience  
- Enhanced overall usability and workflow smoothness  

### Version 1.0

- Initial release  
- Click or drag to open Street View  
- Right-click context menu integration  
- CRS support with auto WGS84 transformation  
- ESC key cancellation  
- Auto return to selection mode  

---

## Contributing

Contributions are welcome.

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Push to your branch  
5. Open a Pull Request  

---

## Issues & Feature Requests

Found a bug or want to suggest an improvement?  
Open an issue on GitHub.

---

## Author

**MD Moinul Mobin**  
GIS Specialist  
Email: mdmoinulmobin@gmail.com  
GitHub: https://github.com/md-moinul-mobin/StreetView-Pro  

---

## License

This project is licensed under the MIT License.

---

## Support

If you find this plugin useful:

- Star the repository  
- Share it with colleagues  
- Submit feedback or suggestions  

---

**Note:** This plugin opens Google Street View in your browser. Please ensure compliance with Google’s Terms of Service when using Street View data.
