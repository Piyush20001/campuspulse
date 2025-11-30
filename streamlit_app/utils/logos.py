"""
Logo and branding assets for Campus Pulse
"""

# UF Logo (Official)
UF_LOGO_URL = "https://i.imgur.com/5bZvhKL.png"  # UF official logo

# Campus Pulse Logo SVG (embedded as data URL)
CAMPUS_PULSE_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" style="height: 50px; width: auto;">
  <defs>
    <linearGradient id="pulseGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0021A5;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FA4616;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Outer circle with gradient -->
  <circle cx="100" cy="100" r="85" fill="url(#pulseGradient)" opacity="0.8"/>

  <!-- Pulse rings -->
  <circle cx="100" cy="100" r="70" fill="none" stroke="white" stroke-width="3" opacity="0.6"/>
  <circle cx="100" cy="100" r="55" fill="none" stroke="white" stroke-width="2" opacity="0.4"/>
  <circle cx="100" cy="100" r="40" fill="none" stroke="white" stroke-width="1" opacity="0.3"/>

  <!-- Center dot -->
  <circle cx="100" cy="100" r="25" fill="white" filter="url(#glow)"/>

  <!-- Heart icon representing campus activity -->
  <path d="M100 125 Q85 100 70 100 Q55 100 55 115 Q55 130 100 165 Q145 130 145 115 Q145 100 130 100 Q115 100 100 125"
        fill="#0021A5" stroke="#0021A5" stroke-width="1"/>
</svg>
"""

# Alternative: Heat map icon SVG
HEATMAP_ICON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" style="height: 45px; width: auto;">
  <defs>
    <radialGradient id="heatGradient">
      <stop offset="0%" style="stop-color:#FA4616;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#FFA500;stop-opacity:0.7" />
      <stop offset="100%" style="stop-color:#0021A5;stop-opacity:0.3" />
    </radialGradient>
  </defs>

  <!-- Map pin -->
  <path d="M100 30 Q70 30 55 55 Q40 80 40 100 Q40 130 100 170 Q160 130 160 100 Q160 80 145 55 Q130 30 100 30"
        fill="url(#heatGradient)" stroke="#0021A5" stroke-width="3"/>

  <!-- Inner circle -->
  <circle cx="100" cy="90" r="25" fill="white" opacity="0.9"/>
  <circle cx="100" cy="90" r="15" fill="#FA4616"/>
</svg>
"""

def get_uf_logo_html():
    """Get UF logo as HTML img tag"""
    return f'<img src="{UF_LOGO_URL}" class="navbar-logo" alt="University of Florida" />'

def get_campus_pulse_logo_html():
    """Get Campus Pulse logo as inline SVG"""
    return CAMPUS_PULSE_LOGO_SVG

def get_heatmap_icon_html():
    """Get heatmap icon as inline SVG"""
    return HEATMAP_ICON_SVG
