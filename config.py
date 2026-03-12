"""
Configuration for chart styling, colors, fonts, and paths
"""
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

# Get the project root directory (parent of this file)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Default data directory
DATA_DIR = PROJECT_ROOT.parent / 'tracking'

# Default output directory
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')

# Archive directory for old charts
ARCHIVE_DIR = os.path.join(OUTPUT_DIR, 'archive')

# Font directory

FONT_DIR = os.path.join(PROJECT_ROOT, '.fonts')

# Create directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Default input files
DEFAULT_PI_FILE = os.path.join(DATA_DIR, 'pi_organization_totals.txt')
DEFAULT_USER_FILE = os.path.join(DATA_DIR, 'user_organization_totals.txt')

# ============================================================================
# FONT CONFIGURATION
# ============================================================================

# Roboto font path
FONT_PATH = os.path.join(FONT_DIR, 'Roboto/static/Roboto-Medium.ttf')

# '/projects/bprogers/main/saracook/carina_charts/.fonts/Roboto/static/Roboto-Medium.ttf'

def configure_fonts():
    """Configure matplotlib to use Roboto font"""
    
    # Check if font file exists
    if os.path.exists(FONT_PATH):
        try:
            # Add the font to matplotlib's font manager
            fm.fontManager.addfont(FONT_PATH)
            
            # Get the font properties
            prop = fm.FontProperties(fname=FONT_PATH)
            font_name = prop.get_name()
            
            # Set as default font
            plt.rcParams['font.family'] = font_name
            print(f"✓ Loaded custom font: {font_name}")
            
        except Exception as e:
            print(f"⚠ Warning: Could not load font from {FONT_PATH}: {e}")
            print("  Falling back to default sans-serif fonts")
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    else:
        print(f"⚠ Warning: Font file not found at {FONT_PATH}")
        print("  Falling back to default sans-serif fonts")
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    
    # Set default font sizes for different elements
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 11
    plt.rcParams['figure.titlesize'] = 18

# ============================================================================
# COLOR PALETTES
# ============================================================================

STANFORD_COLORS = [
    '#8C1515',  # Cardinal Red
    '#007C92',  # Lagunita
    '#E04F39',  # Spirited
    '#175E54',  # Palo Alto
    '#FEC51D',  # Yellow (dk)
    '#734675',  # Lt Plum
    '#016895',  # sky
    '#E98300',  # Poppy
    '#B1040E',  # Dark Red
    '#0098DB',  # Bright Blue
    '#D1660F',  # Dark Poppy
    '#006B54',  # Green
    '#4D4F53',  # Dark Grey
    '#59B3A9',  # lt palo verde

]

COLORBLIND_SAFE = [
    '#0173B2',  # Blue
    '#DE8F05',  # Orange
    '#029E73',  # Green
    '#CC78BC',  # Purple
    '#CA9161',  # Tan
    '#949494',  # Grey
    '#ECE133',  # Yellow
    '#56B4E9',  # Sky Blue
    '#029E73',  # Teal
    '#D55E00',  # Vermillion
]

VIRIDIS_PALETTE = [
    '#440154',  # Dark Purple
    '#443A83',  # Purple
    '#31688E',  # Blue
    '#21908C',  # Teal
    '#35B779',  # Green
    '#8FD744',  # Light Green
    '#FDE724',  # Yellow
]

HIGH_CONTRAST = [
    '#1f77b4',  # Blue
    '#d62728',  # Red
    '#2ca02c',  # Green
    '#9467bd',  # Purple
    '#8c564b',  # Brown
    '#e377c2',  # Pink
    '#7f7f7f',  # Grey
    '#17becf',  # Cyan
    '#bcbd22',  # Olive
    '#ff7f0e',  # Orange
    '#8B0000',  # Dark Red
    '#006400',  # Dark Green
]

COLOR_PALETTES = {
    'stanford': STANFORD_COLORS,
    'colorblind': COLORBLIND_SAFE,
    'viridis': VIRIDIS_PALETTE,
    'high_contrast': HIGH_CONTRAST
}
