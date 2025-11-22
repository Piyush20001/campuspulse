# Campus Pulse Image Assets

This directory contains image files used throughout the Campus Pulse application.

## 📁 Directory Structure

```
streamlit_app/assets/images/
├── uf_logo.png              # University of Florida official logo
├── campus_pulse_logo.png    # Campus Pulse branded logo
├── favicon.ico              # Browser favicon
└── README.md                # This file
```

## 🖼️ Required Images

### 1. **uf_logo.png**
- **Description**: Official University of Florida logo
- **Recommended Size**: 200x200px (or larger)
- **Format**: PNG with transparent background
- **Used In**: Top navigation bar
- **Where to get it**: Download from UF Brand Center or use the official UF logo

### 2. **campus_pulse_logo.png** (Optional)
- **Description**: Campus Pulse branded logo
- **Recommended Size**: 100x100px
- **Format**: PNG with transparent background
- **Used In**: Top navigation bar (next to UF logo)
- **Note**: If not provided, an SVG thermal heatmap icon will be used

### 3. **favicon.ico** (Optional)
- **Description**: Browser tab icon
- **Recommended Size**: 32x32px or 16x16px
- **Format**: ICO
- **Used In**: Browser tabs
- **Note**: Not currently implemented but reserved for future use

## 📥 How to Add Your Images

### Step 1: Get Your Images
Download or create your logo images. For UF logo, you can:
- Download from UF Brand Center: https://brand.ufl.edu
- Use the official UF Athletics logo
- Use any UF-approved branding

### Step 2: Place Images in This Directory
```bash
# From your project root
cd streamlit_app/assets/images/

# Copy your images here
cp /path/to/your/uf_logo.png .
cp /path/to/your/campus_pulse_logo.png .
```

### Step 3: Images Will Be Auto-Loaded
The application will automatically:
1. Try to load from this directory first
2. Fall back to external URLs if files not found
3. Encode images as base64 for embedding in HTML

## 🔧 Technical Details

### Image Loading Process
1. `image_utils.py` checks for images in this directory
2. If found, converts to base64 encoding
3. Embeds directly in HTML for faster loading
4. If not found, falls back to external URLs

### Supported Formats
- **PNG** (recommended for logos with transparency)
- **JPG/JPEG** (for photos)
- **SVG** (for vector graphics)
- **GIF** (for animations)
- **ICO** (for favicons)

### Why Base64 Encoding?
Streamlit doesn't serve static files the same way traditional web servers do. Base64 encoding allows us to:
- Embed images directly in HTML
- Avoid CORS issues
- Improve loading performance
- Work in any deployment environment

## 📝 Image Specifications

### UF Logo
```
Filename: uf_logo.png
Dimensions: 200x200px (minimum)
Background: Transparent
Format: PNG
Colors: UF Blue (#0021A5), Orange (#FA4616)
```

### Campus Pulse Logo
```
Filename: campus_pulse_logo.png
Dimensions: 100x100px (minimum)
Background: Transparent
Format: PNG
Theme: Thermal/heatmap style (optional)
Colors: Orange (#FA4616), Blue (#0021A5)
```

## 🎨 Creating Campus Pulse Logo

If you want to create a custom Campus Pulse logo, consider:

**Design Elements:**
- Thermal/heatmap gradient (red/orange center, blue edges)
- Pin/marker shape (represents locations)
- Pulse/wave design (represents activity)
- Circular with concentric rings (represents data spreading)

**Color Scheme:**
- Primary: UF Blue (#0021A5)
- Secondary: UF Orange (#FA4616)
- Accent: Golden yellow (#FFD700)

**Tools:**
- Adobe Illustrator
- Figma
- Canva
- GIMP (free)

## 🔄 Fallback Behavior

If images are not found in this directory:

1. **UF Logo**: Falls back to `https://i.imgur.com/5bZvhKL.png`
2. **Campus Pulse Logo**: Falls back to SVG thermal heatmap icon (rendered inline)

This ensures the app always looks good, even without custom images.

## 📊 Current Status

Check which images are loaded:
```python
from utils.image_utils import get_assets_path

assets_path = get_assets_path()
print(f"Looking for images in: {assets_path}")
print(f"UF Logo exists: {(assets_path / 'uf_logo.png').exists()}")
print(f"Campus Pulse Logo exists: {(assets_path / 'campus_pulse_logo.png').exists()}")
```

## 🚀 Quick Start

```bash
# 1. Download UF logo
# Go to: https://brand.ufl.edu/resources/

# 2. Save to this directory
# Save as: streamlit_app/assets/images/uf_logo.png

# 3. Restart the app
streamlit run streamlit_app/app.py

# Your logo will now appear in the navigation bar!
```

## 💡 Tips

1. **Use PNG with transparency** for logos (not JPG)
2. **Keep file sizes small** (<500KB) for faster loading
3. **Use high resolution** (2x) for retina displays
4. **Name files exactly** as specified (case-sensitive)
5. **Test in both themes** (light and dark) to ensure visibility

## 📧 Need Help?

If you're having trouble with images:
1. Check file names match exactly
2. Verify file permissions (readable)
3. Ensure images are in correct format
4. Check terminal for error messages
5. Try the fallback URLs first to test layout

---

**Built for University of Florida • Campus Pulse**

🐊 Go Gators! 🐊
