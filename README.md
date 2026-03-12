# Chart Generator

Professional data visualization tool for generating storage usage charts from Carina cluster organization data at Stanford University.

## 📋 Overview

Carina Charts creates beautiful, publication-ready visualizations of storage usage data across PI (Principal Investigator) and User organizations. The tool generates multiple chart types with Stanford branding and supports archiving of previous outputs.

## 🎯 Features

- **Multiple Chart Types**
  - Pie charts with legends
  - Horizontal bar charts
  - Professional data tables
  - Combined pie + table views
  - PI vs User comparison charts

- **Stanford Branding**
  - Custom Stanford color palettes
  - Roboto font integration
  - Professional styling

- **Smart Archiving**
  - Automatic timestamped backups
  - Configurable retention policy
  - Clean output directory management

- **Flexible Configuration**
  - Multiple color palette options
  - Customizable chart settings
  - Easy font and style configuration

## 📁 Project Structure

```
tracking/                            # Data files (parent directory)
├── pi_organization_totals.txt
└── user_organization_totals.txt

carina_charts/                       # Main project directory
├── charts/                          # Chart generation modules
│   ├── __init__.py
│   ├── pie.py                      # Pie chart with legend
│   ├── bar.py                      # Horizontal bar chart
│   ├── table.py                    # Professional table
│   ├── combined.py                 # Pie + table side-by-side
│   └── comparison.py               # PI vs User comparison
├── output/                         # Generated charts (CHARTS APPEAR HERE)
│   └── archive/                    # Old charts archived here
│       ├── archive_20260311_093000/
│       └── archive_20260311_101500/
├── .fonts/                         # Custom fonts
│   └── Roboto/
│       └── static/
│           └── Roboto-Medium.ttf
├── config.py                       # Configuration (colors, fonts, paths)
├── utils.py                        # Utility functions
├── archive.py                      # Archiving utilities
├── main.py                         # Main script (RUN THIS)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10 or higher
- Conda (recommended) or pip

### 2. Installation

#### Using Conda (Recommended)

```bash
# Create and activate environment
conda create -n charts python=3.10 -y
conda activate charts

# Install dependencies
pip install -r requirements.txt
```

#### Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Activate environment
conda activate charts

# Run main script
python main.py
```

Or use the provided bash script:

```bash
chmod +x run_charts.sh
./run_charts.sh
```

### 4. View Output

Charts are saved to `carina_charts/output/`:
- `pi_org_pie.png` - PI organization pie chart
- `user_org_pie.png` - User organization pie chart
- `pi_org_bar.png` - PI organization bar chart
- `user_org_bar.png` - User organization bar chart
- `pi_org_table.png` - PI organization table
- `user_org_table.png` - User organization table
- `pi_org_combined.png` - PI pie + table combined
- `user_org_combined.png` - User pie + table combined
- `pi_vs_user_comparison.png` - Side-by-side comparison

## ⚙️ Configuration

Edit `config.py` to customize:

### Color Palettes

Choose from predefined palettes:
```python
DEFAULT_PALETTE = 'stanford'  # Options: 'stanford', 'colorblind', 'viridis', 'high_contrast'
```

### Chart Settings

```python
FIGURE_SIZE_PIE = (12, 8)        # Chart dimensions
DPI = 300                         # Image resolution
PERCENTAGE_THRESHOLD = 2.0        # Min % to show on pie chart
```

### Archive Settings

```python
ARCHIVE_KEEP_LATEST = 10         # Number of archives to keep
```

### Data File Locations

```python
DEFAULT_PI_FILE = DATA_DIR / 'pi_organization_totals.txt'
DEFAULT_USER_FILE = DATA_DIR / 'user_organization_totals.txt'
```

## 📊 Data Format

Input files should be tab-separated with two columns:

```
Organization_Name	Storage_Value
Biology_Lab	1500
Chemistry_Dept	2300
Physics_Center	1800
```

## 🎨 Color Palettes

### Stanford (Default)
Official Stanford colors including Cardinal Red, Lagunita, and complementary colors.

### Colorblind Safe
Carefully selected colors optimized for colorblind accessibility.

### Viridis
Perceptually uniform color scheme from dark to light.

### High Contrast
Maximum visual distinction between adjacent categories.

## 📦 Dependencies

```
matplotlib>=3.5.0
numpy>=1.21.0
pandas>=1.3.0
```

See `requirements.txt` for complete list.

## 🔧 Troubleshooting

### Font Issues

If custom fonts don't load:
1. Check that `.fonts/Roboto/static/Roboto-Medium.ttf` exists
2. The app will automatically fall back to system fonts
3. You'll see a warning message indicating the fallback

### Data File Not Found

If you see "File not found" errors:
1. Verify `tracking/` directory is at the same level as `carina_charts/`
2. Check that data files exist in `tracking/`
3. Verify file permissions

### Missing Output Directory

The app automatically creates `output/` and `output/archive/` directories.

## 📝 Usage Examples

### Generate All Charts

```bash
python main.py
```

### Generate Specific Chart Types

```python
from charts import pie, bar, table, combined, comparison
from utils import load_data

# Load data
pi_data = load_data('path/to/pi_data.txt')
user_data = load_data('path/to/user_data.txt')

# Generate specific chart
pie.create_pie_chart(pi_data, 'output/my_pie.png', title='My Custom Title')
```

### Custom Colors

```python
from config import COLOR_PALETTES

# Use different palette
custom_colors = COLOR_PALETTES['colorblind']
pie.create_pie_chart(data, 'output.png', colors=custom_colors)
```


## 🔄 Version History

- **v1.0** - Initial release with pie, bar, table, combined, and comparison charts
- Stanford color palette integration
- Automatic archiving system
- Font customization support

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review configuration in `config.py`
- Verify data file format matches expected structure

---

**Last Updated:** March 2026  
