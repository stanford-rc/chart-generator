"""
Professional table visualization
"""
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_text_color
from config import HIGH_CONTRAST

def create_table(departments, counts, output_file, title_suffix="", color_palette=None):
    """Create a professional table visualization"""
    if color_palette is None:
        color_palette = HIGH_CONTRAST
    
    # Sort by count descending
    sorted_data = sorted(zip(departments, counts), key=lambda x: x[1], reverse=True)
    departments_sorted, counts_sorted = zip(*sorted_data)
    
    # Calculate percentages
    total = sum(counts_sorted)
    percentages = [(count / total) * 100 for count in counts_sorted]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare table data
    table_data = []
    for i, (dept, count, pct) in enumerate(zip(departments_sorted, counts_sorted, percentages), 1):
        table_data.append([i, dept, count, f'{pct:.1f}%'])
    
    # Add total row
    table_data.append(['', 'TOTAL', total, '100.0%'])
    
    # Create table
    table = ax.table(
        cellText=table_data,
        colLabels=['Rank', 'Department/School', 'Count', 'Percentage'],
        cellLoc='left',
        loc='center',
        colWidths=[0.08, 0.62, 0.15, 0.15]
    )
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Header styling - use color from palette
    header_color = color_palette[0]
    header_text_color = get_text_color(header_color)
    for i in range(4):
        cell = table[(0, i)]
        cell.set_facecolor(header_color)
        cell.set_text_props(weight='bold', color=header_text_color, fontsize=12)
        cell.set_edgecolor('white')
        cell.set_linewidth(2)
    
    # Alternate row colors
    for i in range(1, len(table_data) + 1):
        for j in range(4):
            cell = table[(i, j)]
            cell.set_edgecolor('white')
            cell.set_linewidth(1)
            
            if i == len(table_data):  # Total row
                cell.set_facecolor('#E7E6E6')
                cell.set_text_props(weight='bold', fontsize=11)
            elif i % 2 == 0:
                cell.set_facecolor('#F8F8F8')
            else:
                cell.set_facecolor('white')
            
            # Right-align numbers
            if j in [0, 2, 3]:
                cell.set_text_props(ha='right')
    
    # Add title
    plt.title(f'Carina Cluster {title_suffix} by Department/School',
              fontsize=18, weight='bold', pad=20)
    
    # Add timestamp
    timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    plt.figtext(0.5, 0.02, f'Generated: {timestamp_str}',
                ha='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Table saved as: {output_file}")
