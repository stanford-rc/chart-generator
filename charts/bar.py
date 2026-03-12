"""
Horizontal bar chart creation
"""
import sys
import os
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_text_color
from config import HIGH_CONTRAST

def create_bar_chart(departments, counts, output_file, title_suffix="", color_palette=None):
    """Create a horizontal bar chart with custom colors"""
    if color_palette is None:
        color_palette = HIGH_CONTRAST
    
    fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
    
    # Sort by count descending
    sorted_data = sorted(zip(departments, counts), key=lambda x: x[1], reverse=True)
    departments_sorted, counts_sorted = zip(*sorted_data)
    
    # Use primary color from palette for bars
    bar_color = color_palette[0]
    
    # Create horizontal bar chart
    bars = ax.barh(departments_sorted, counts_sorted, color=bar_color, 
                   edgecolor='white', linewidth=0.5)
    
    # Add value labels on bars with contrasting color
    text_color = get_text_color(bar_color)
    for i, (bar, count) in enumerate(zip(bars, counts_sorted)):
        width = bar.get_width()
        # Put label inside bar if it's wide enough, otherwise outside
        if width > max(counts_sorted) * 0.1:
            ax.text(width * 0.95, bar.get_y() + bar.get_height()/2,
                    f'{count}',
                    ha='right', va='center', fontsize=10, weight='bold', color=text_color)
        else:
            ax.text(width + max(counts_sorted) * 0.01, bar.get_y() + bar.get_height()/2,
                    f'{count}',
                    ha='left', va='center', fontsize=10, weight='bold', color='black')
    
    ax.set_xlabel('Count', fontsize=14, weight='bold')
    ax.set_title(f'Distribution by Department/School\nCarina {title_suffix}',
                 fontsize=16, weight='bold', pad=15)
    ax.grid(axis='x', alpha=0.3, linestyle='--', color='gray')
    ax.set_axisbelow(True)
    
    # Style the spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Bar chart saved as: {output_file}")
