"""
Side-by-side comparison chart for PI vs User data
"""
import sys
import os
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_text_color
from config import HIGH_CONTRAST

def create_comparison_chart(pi_data, user_data, output_file, color_palette=None):
    """Create a side-by-side comparison of PI vs User counts"""
    if color_palette is None:
        color_palette = HIGH_CONTRAST
    
    pi_depts, pi_counts = pi_data
    user_depts, user_counts = user_data
    
    # Get all unique departments
    all_depts = sorted(set(pi_depts + user_depts))
    
    # Create dictionaries for easy lookup
    pi_dict = dict(zip(pi_depts, pi_counts))
    user_dict = dict(zip(user_depts, user_counts))
    
    # Prepare data for comparison
    pi_values = [pi_dict.get(dept, 0) for dept in all_depts]
    user_values = [user_dict.get(dept, 0) for dept in all_depts]
    
    # Sort by total (PI + User) descending
    combined = list(zip(all_depts, pi_values, user_values))
    combined.sort(key=lambda x: x[1] + x[2], reverse=True)
    all_depts, pi_values, user_values = zip(*combined)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
    
    y_pos = range(len(all_depts))
    bar_height = 0.35
    
    # Use colors from palette
    pi_color = color_palette[0]  # First color for PIs
    user_color = color_palette[2]  # Third color for Users (for better contrast)
    
    # Create bars
    bars1 = ax.barh([y - bar_height/2 for y in y_pos], pi_values, 
                     bar_height, label='PIs', color=pi_color, alpha=0.9, 
                     edgecolor='white', linewidth=0.5)
    bars2 = ax.barh([y + bar_height/2 for y in y_pos], user_values, 
                     bar_height, label='Users', color=user_color, alpha=0.9, 
                     edgecolor='white', linewidth=0.5)
    
    # Add value labels with contrasting colors
    pi_text_color = get_text_color(pi_color)
    user_text_color = get_text_color(user_color)
    
    max_value = max(max(pi_values), max(user_values))
    
    for bar, color, text_color in [(bars1, pi_color, pi_text_color), 
                                    (bars2, user_color, user_text_color)]:
        for b in bar:
            width = b.get_width()
            if width > 0:
                # Put label inside if bar is wide enough
                if width > max_value * 0.1:
                    ax.text(width * 0.95, b.get_y() + b.get_height()/2,
                           f'{int(width)}',
                           ha='right', va='center', fontsize=9, weight='bold', 
                           color=text_color)
                else:
                    ax.text(width + max_value * 0.01, 
                           b.get_y() + b.get_height()/2,
                           f'{int(width)}',
                           ha='left', va='center', fontsize=9, weight='bold', 
                           color='black')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(all_depts, fontsize=10)
    ax.set_xlabel('Count', fontsize=14, weight='bold')
    ax.set_title('PI vs User Distribution by Department/School\nCarina',
                 fontsize=16, weight='bold', pad=15)
    ax.legend(loc='lower right', fontsize=12, frameon=True, shadow=True)
    ax.grid(axis='x', alpha=0.3, linestyle='--', color='gray')
    ax.set_axisbelow(True)
    
    # Style the spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add totals
    total_pi = sum(pi_values)
    total_users = sum(user_values)
    plt.figtext(0.5, 0.02, 
                f'Total PIs: {total_pi} | Total Users: {total_users}',
                ha='center', fontsize=12, style='italic', weight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Comparison chart saved as: {output_file}")
