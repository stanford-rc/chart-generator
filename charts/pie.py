"""
Pie chart creation with legend and conditional labels
"""
import sys
import os
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_text_color
from config import HIGH_CONTRAST

def create_pie_chart(departments, counts, output_file, title_suffix="", 
                    min_pct_label=2.0, color_palette=None, legend_fontsize=12):
    """Create a pie chart with legend and conditional percentage labels"""
    if color_palette is None:
        color_palette = HIGH_CONTRAST
    
    # Sort by count descending
    sorted_data = sorted(zip(departments, counts), key=lambda x: x[1], reverse=True)
    departments_sorted, counts_sorted = zip(*sorted_data)
    
    total = sum(counts_sorted)
    percentages = [(count / total) * 100 for count in counts_sorted]
    
    fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
    
    # Cycle through colors if we have more slices than colors
    num_slices = len(departments_sorted)
    colors = [color_palette[i % len(color_palette)] for i in range(num_slices)]
    
    # Custom autopct function with configurable threshold
    def autopct_format(pct):
        return f'{pct:.1f}%' if pct >= min_pct_label else ''
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        counts_sorted,
        autopct=autopct_format,
        startangle=90,
        colors=colors,
        pctdistance=0.85,
        explode=[0.05 if i == 0 else 0 for i in range(len(counts_sorted))]
    )
    
    # Style percentage text with appropriate color based on background
    for autotext, color in zip(autotexts, colors):
        text_color = get_text_color(color)
        autotext.set_color(text_color)
        autotext.set_fontsize(12)
        autotext.set_weight('bold')
    
    # Create legend with department names and counts
    legend_labels = []
    for dept, count, pct in zip(departments_sorted, counts_sorted, percentages):
        legend_labels.append(f'{dept}: {count} ({pct:.1f}%)')
    
    # Position legend to the right with larger font
    ax.legend(
        wedges,
        legend_labels,
        title="Department/School",
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        fontsize=legend_fontsize,
        title_fontsize=legend_fontsize + 2,
        frameon=True,
        fancybox=True,
        shadow=True
    )
    
    plt.title(f'Distribution by Department/School\nCarina Cluster {title_suffix}',
              fontsize=20, weight='bold', pad=20)
    ax.axis('equal')
    
    plt.figtext(0.5, 0.02, f'Total: {total}',
                ha='center', fontsize=13, style='italic', weight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Pie chart saved as: {output_file}")
