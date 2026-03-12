"""
Combined visualization with pie chart and table side-by-side
"""
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_text_color
from config import HIGH_CONTRAST

def create_combined_chart(departments, counts, output_file, title_suffix="",
                         min_pct_label=2.0, color_palette=None, legend_fontsize=11):
    """Create a combined visualization with pie chart and table"""
    if color_palette is None:
        color_palette = HIGH_CONTRAST
    
    # Sort by count descending
    sorted_data = sorted(zip(departments, counts), key=lambda x: x[1], reverse=True)
    departments_sorted, counts_sorted = zip(*sorted_data)
    
    total = sum(counts_sorted)
    percentages = [(count / total) * 100 for count in counts_sorted]
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 10), dpi=100)
    
    # Pie chart on the left
    ax1 = plt.subplot(1, 2, 1)
    
    # Cycle through colors
    num_slices = len(departments_sorted)
    colors = [color_palette[i % len(color_palette)] for i in range(num_slices)]
    
    # Custom autopct function
    def autopct_format(pct):
        return f'{pct:.1f}%' if pct >= min_pct_label else ''
    
    wedges, texts, autotexts = ax1.pie(
        counts_sorted,
        autopct=autopct_format,
        startangle=90,
        colors=colors,
        pctdistance=0.85,
        explode=[0.05 if i == 0 else 0 for i in range(len(counts_sorted))]
    )
    
    # Style percentage text with appropriate color
    for autotext, color in zip(autotexts, colors):
        text_color = get_text_color(color)
        autotext.set_color(text_color)
        autotext.set_fontsize(11)
        autotext.set_weight('bold')
    
    # Create legend for pie chart
    legend_labels = []
    for dept, count, pct in zip(departments_sorted, counts_sorted, percentages):
        dept_short = dept if len(dept) <= 35 else dept[:32] + '...'
        legend_labels.append(f'{dept_short} ({count})')
    
    ax1.legend(
        wedges,
        legend_labels,
        title="Department/School",
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        fontsize=legend_fontsize,
        title_fontsize=legend_fontsize + 2,
        frameon=True
    )
    
    ax1.axis('equal')
    
    # Table on the right
    ax2 = plt.subplot(1, 2, 2)
    ax2.axis('tight')
    ax2.axis('off')
    
    # Prepare table data
    table_data = []
    for i, (dept, count, pct) in enumerate(zip(departments_sorted, counts_sorted, percentages), 1):
        dept_short = dept if len(dept) <= 40 else dept[:37] + '...'
        table_data.append([i, dept_short, count, f'{pct:.1f}%'])
    
    table_data.append(['', 'TOTAL', total, '100.0%'])
    
    # Create table
    table = ax2.table(
        cellText=table_data,
        colLabels=['#', 'Department/School', 'Count', '%'],
        cellLoc='left',
        loc='center',
        colWidths=[0.08, 0.62, 0.15, 0.15]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.2)
    
    # Header styling - use color from palette
    header_color = color_palette[0]
    header_text_color = get_text_color(header_color)
    for i in range(4):
        cell = table[(0, i)]
        cell.set_facecolor(header_color)
        cell.set_text_props(weight='bold', color=header_text_color, fontsize=11)
        cell.set_edgecolor('white')
        cell.set_linewidth(2)
    
 # Row styling
    for i in range(1, len(table_data) + 1):
        for j in range(4):
            cell = table[(i, j)]
            cell.set_edgecolor('white')
            cell.set_linewidth(1)
            
            if i == len(table_data):
                cell.set_facecolor('#E7E6E6')
                cell.set_text_props(weight='bold')
            elif i % 2 == 0:
                cell.set_facecolor('#F8F8F8')
            else:
                cell.set_facecolor('white')
            
            if j in [0, 2, 3]:
                cell.set_text_props(ha='right')
    
    # Overall title
    fig.suptitle(f'Carina {title_suffix} by Department/School',
                 fontsize=20, weight='bold', y=0.98)
    
    timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    plt.figtext(0.5, 0.02, f'Total: {total} | Generated: {timestamp_str}',
                ha='center', fontsize=11)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Combined chart saved as: {output_file}")
