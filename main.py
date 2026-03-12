#!/usr/bin/env python3
"""
Main script for creating organization charts
Usage: python main.py --help
"""
import argparse
import os
from datetime import datetime

from config import (
    configure_fonts, 
    COLOR_PALETTES, 
    DEFAULT_PI_FILE, 
    DEFAULT_USER_FILE,
    OUTPUT_DIR,
    ARCHIVE_DIR,
    FONT_PATH
)
from utils import read_data, print_summary
from archive import archive_existing_charts, clean_old_archives, print_archive_summary
from charts import (
    create_pie_chart,
    create_bar_chart,
    create_table,
    create_combined_chart,
    create_comparison_chart
)

def main():
    parser = argparse.ArgumentParser(
        description='Create charts and tables from organization data'
    )
    parser.add_argument('--pi-file', 
                        default=DEFAULT_PI_FILE,
                        help=f'PI organization file (default: {DEFAULT_PI_FILE})')
    parser.add_argument('--user-file', 
                        default=DEFAULT_USER_FILE,
                        help=f'User organization file (default: {DEFAULT_USER_FILE})')
    parser.add_argument('--output-dir', 
                        default=OUTPUT_DIR,
                        help=f'Output directory for charts (default: {OUTPUT_DIR})')
    parser.add_argument('--archive-dir',
                        default=ARCHIVE_DIR,
                        help=f'Archive directory (default: {ARCHIVE_DIR})')
    parser.add_argument('--font-path',
                        default=FONT_PATH,
                        help=f'Path to custom font file (default: {FONT_PATH})')
    parser.add_argument('--type', 
                        choices=['pie', 'bar', 'table', 'combined', 'comparison', 'all'], 
                        default='all',
                        help='Type of visualization to create (default: all)')
    parser.add_argument('--output-prefix', 
                        default='carina_org',
                        help='Output file prefix (default: carina_org)')
    parser.add_argument('--process', 
                        choices=['pi', 'user', 'both'], 
                        default='both',
                        help='Which data to process (default: both)')
    parser.add_argument('--colors', 
                        choices=['stanford', 'colorblind', 'viridis', 'high_contrast'],
                        default='high_contrast',
                        help='Color palette to use (default: high_contrast)')
    parser.add_argument('--min-pct-label', 
                        type=float, 
                        default=2.0,
                        help='Minimum percentage to show label on pie chart (default: 2.0)')
    parser.add_argument('--legend-fontsize', 
                        type=int, 
                        default=12,
                        help='Font size for pie chart legend (default: 12)')
    parser.add_argument('--no-archive', 
                        action='store_true',
                        help='Skip archiving existing charts')
    parser.add_argument('--keep-archives', 
                        type=int, 
                        default=10,
                        help='Number of old archives to keep (default: 10)')
    parser.add_argument('--list-archives', 
                        action='store_true',
                        help='List available archives and exit')
    
    args = parser.parse_args()
    
    # Handle --list-archives command
    if args.list_archives:
        print_archive_summary(args.archive_dir)
        return
    
    # Configure fonts globally (with optional custom font path)
    if args.font_path != FONT_PATH:
        # Update the config module's font path if user provided one
        import config
        config.FONT_PATH = args.font_path
    
    configure_fonts()
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.archive_dir, exist_ok=True)
    
    # Archive existing charts before creating new ones
    if not args.no_archive:
        archived = archive_existing_charts(
            args.output_dir, 
            args.archive_dir, 
            args.output_prefix
        )
        
        # Clean up old archives if any files were archived
        if archived > 0:
            clean_old_archives(args.archive_dir, keep_count=args.keep_archives)
    
    # Select color palette
    selected_palette = COLOR_PALETTES[args.colors]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Read data files with error handling
    pi_data = None
    user_data = None
    
    if args.process in ['pi', 'both']:
        if not os.path.exists(args.pi_file):
            print(f"ERROR: PI file not found: {args.pi_file}")
            return
        print(f"Reading PI data from {args.pi_file}...")
        pi_depts, pi_counts = read_data(args.pi_file)
        pi_data = (pi_depts, pi_counts)
    
    if args.process in ['user', 'both']:
        if not os.path.exists(args.user_file):
            print(f"ERROR: User file not found: {args.user_file}")
            return
        print(f"Reading User data from {args.user_file}...")
        user_depts, user_counts = read_data(args.user_file)
        user_data = (user_depts, user_counts)
    
    # Process PI data
    if pi_data and args.process in ['pi', 'both']:
        pi_depts, pi_counts = pi_data
        
        if args.type in ['pie', 'all']:
            output_file = os.path.join(args.output_dir, f'{args.output_prefix}_pi_pie_{timestamp}.png')
            print(f"\nCreating PI pie chart...")
            create_pie_chart(pi_depts, pi_counts, output_file, "PI Distribution",
                           args.min_pct_label, selected_palette, args.legend_fontsize)
        
        if args.type in ['bar', 'all']:
            output_file = os.path.join(args.output_dir, f'{args.output_prefix}_pi_bar_{timestamp}.png')
            print(f"\nCreating PI bar chart...")
            create_bar_chart(pi_depts, pi_counts, output_file, "PI Distribution", selected_palette)
        
        if args.type in ['table', 'all']:
            output_file = os.path.join(args.output_dir, f'{args.output_prefix}_pi_table_{timestamp}.png')
            print(f"\nCreating PI table...")
            create_table(pi_depts, pi_counts, output_file, "PI Distribution", selected_palette)
        
        if args.type in ['combined', 'all']:
            output_file = os.path.join(args.output_dir, f'{args.output_prefix}_pi_combined_{timestamp}.png')
            print(f"\nCreating PI combined visualization...")
            create_combined_chart(pi_depts, pi_counts, output_file, "PI Distribution",
                                args.min_pct_label, selected_palette, args.legend_fontsize)
        
        print_summary(pi_depts, pi_counts, "PI")
    
    # Process User data
    if user_data and args.process in ['user', 'both']:
        user_depts, user_counts = user_data
        
        if args.type in ['pie', 'all']:
            output_file = os.path.join(args.output_dir, f'{args.output_prefix}_user_pie_{timestamp}.png')
            print(f"\nCreating User pie chart...")
            create_pie_chart(user_depts, user_counts, output_file, "User Distribution",
                           args.min_pct_label, selected_palette, args.legend_fontsize)
        
        if args.type in ['bar', 'all']:
            output_file = os.path.join(args.output_dir, f'{args.output_prefix}_user_bar_{timestamp}.png')
            print(f"\nCreating User bar chart...")
            create_bar_chart(user_depts, user_counts, output_file, "User Distribution", selected_palette)
        
        if args.type in ['table', 'all']:
            output_file = os.path.join(args.output_dir, f'{args.output_prefix}_user_table_{timestamp}.png')
            print(f"\nCreating User table...")
            create_table(user_depts, user_counts, output_file, "User Distribution", selected_palette)
        
        if args.type in ['combined', 'all']:
            output_file = os.path.join(args.output_dir, f'{args.output_prefix}_user_combined_{timestamp}.png')
            print(f"\nCreating User combined visualization...")
            create_combined_chart(user_depts, user_counts, output_file, "User Distribution",
                                args.min_pct_label, selected_palette, args.legend_fontsize)
        
        print_summary(user_depts, user_counts, "User")
    
    # Create comparison chart if both datasets are loaded
    if pi_data and user_data and args.type in ['comparison', 'all']:
        output_file = os.path.join(args.output_dir, f'{args.output_prefix}_comparison_{timestamp}.png')
        print(f"\nCreating PI vs User comparison chart...")
        create_comparison_chart(pi_data, user_data, output_file, selected_palette)
    
    print("\n" + "="*70)
    print(f"All visualizations complete! Check {args.output_dir}/ for output files.")
    print("="*70)

if __name__ == '__main__':
    main()
