"""
Image utilities for Campus Pulse
Handles loading and encoding images for use in Streamlit
"""
import base64
import os
from pathlib import Path


def get_assets_path():
    """Get the path to the assets directory"""
    current_dir = Path(__file__).parent.parent
    return current_dir / "assets" / "images"


def get_base64_image(image_filename):
    """
    Convert an image file to base64 encoding for embedding in HTML

    Args:
        image_filename: Name of the image file (e.g., 'uf_logo.png')

    Returns:
        Base64 encoded string of the image, or None if file not found
    """
    try:
        image_path = get_assets_path() / image_filename

        if not image_path.exists():
            print(f"Warning: Image not found at {image_path}")
            return None

        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()

        # Determine image type from extension
        ext = image_path.suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon'
        }

        mime_type = mime_types.get(ext, 'image/png')

        return f"data:{mime_type};base64,{encoded}"

    except Exception as e:
        print(f"Error encoding image {image_filename}: {str(e)}")
        return None


def get_image_html(image_filename, alt_text="", css_class="", style="", fallback_url=None):
    """
    Get HTML img tag for an image, with fallback to external URL

    Args:
        image_filename: Name of the image file in assets/images/
        alt_text: Alt text for the image
        css_class: CSS class to apply
        style: Inline CSS styles
        fallback_url: External URL to use if local image not found

    Returns:
        HTML img tag as string
    """
    base64_data = get_base64_image(image_filename)

    if base64_data:
        src = base64_data
    elif fallback_url:
        src = fallback_url
    else:
        return f'<!-- Image not found: {image_filename} -->'

    class_attr = f'class="{css_class}"' if css_class else ''
    style_attr = f'style="{style}"' if style else ''

    return f'<img src="{src}" alt="{alt_text}" {class_attr} {style_attr} />'


# Predefined images for easy access
UF_LOGO_FALLBACK = "https://i.imgur.com/5bZvhKL.png"

def get_uf_logo_html(css_class="navbar-logo", style=""):
    """Get UF logo HTML with fallback to external URL"""
    return get_image_html(
        "uf_logo.png",
        alt_text="University of Florida",
        css_class=css_class,
        style=style,
        fallback_url=UF_LOGO_FALLBACK
    )


def get_campus_pulse_logo_html(css_class="navbar-logo", style="height: 45px; width: 45px;"):
    """Get Campus Pulse logo HTML"""
    return get_image_html(
        "campus_pulse_logo.png",
        alt_text="Campus Pulse",
        css_class=css_class,
        style=style,
        fallback_url=None  # Will use SVG fallback
    )
