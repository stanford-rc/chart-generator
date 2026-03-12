"""
Archiving utilities for managing old chart outputs
"""
import os
import shutil
from datetime import datetime
from pathlib import Path


def archive_existing_charts(output_dir, archive_dir, output_prefix='carina_org', verbose=True):
    """
    Move existing chart files to an archive subdirectory with timestamp.
    
    Args:
        output_dir: Directory containing charts to archive
        archive_dir: Base archive directory
        output_prefix: Prefix of files to archive (default: 'carina_org')
        verbose: Print archive operations (default: True)
    
    Returns:
        Number of files archived
    """
    # Find all PNG files matching the output prefix
    output_path = Path(output_dir)
    chart_files = list(output_path.glob(f'{output_prefix}*.png'))
    
    if not chart_files:
        if verbose:
            print("No existing charts found to archive.")
        return 0
    
    # Create timestamped archive subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_subdir = Path(archive_dir) / f'archive_{timestamp}'
    archive_subdir.mkdir(parents=True, exist_ok=True)
    
    # Move files to archive
    archived_count = 0
    if verbose:
        print(f"\nArchiving {len(chart_files)} existing chart(s) to {archive_subdir}...")
    
    for chart_file in chart_files:
        try:
            dest = archive_subdir / chart_file.name
            shutil.move(str(chart_file), str(dest))
            if verbose:
                print(f"  ✓ Archived: {chart_file.name}")
            archived_count += 1
        except Exception as e:
            if verbose:
                print(f"  ✗ Failed to archive {chart_file.name}: {e}")
    
    if verbose:
        print(f"Archived {archived_count} file(s) to {archive_subdir}\n")
    
    return archived_count


def clean_old_archives(archive_dir, keep_count=10, verbose=True):
    """
    Remove old archive directories, keeping only the most recent ones.
    
    Args:
        archive_dir: Base archive directory
        keep_count: Number of most recent archives to keep (default: 10)
        verbose: Print cleanup operations (default: True)
    
    Returns:
        Number of archives deleted
    """
    archive_path = Path(archive_dir)
    
    # Find all archive subdirectories
    archive_subdirs = sorted(
        [d for d in archive_path.iterdir() if d.is_dir() and d.name.startswith('archive_')],
        key=lambda x: x.name,
        reverse=True  # Most recent first
    )
    
    # Determine which to delete
    to_delete = archive_subdirs[keep_count:]
    
    if not to_delete:
        if verbose:
            print(f"No old archives to clean (keeping {keep_count} most recent).")
        return 0
    
    # Delete old archives
    deleted_count = 0
    if verbose:
        print(f"\nCleaning {len(to_delete)} old archive(s) (keeping {keep_count} most recent)...")
    
    for archive_subdir in to_delete:
        try:
            shutil.rmtree(archive_subdir)
            if verbose:
                print(f"  ✓ Deleted: {archive_subdir.name}")
            deleted_count += 1
        except Exception as e:
            if verbose:
                print(f"  ✗ Failed to delete {archive_subdir.name}: {e}")
    
    if verbose:
        print(f"Deleted {deleted_count} old archive(s)\n")
    
    return deleted_count


def list_archives(archive_dir):
    """
    List all available archives with file counts.
    
    Args:
        archive_dir: Base archive directory
    
    Returns:
        List of tuples (archive_name, file_count, timestamp)
    """
    archive_path = Path(archive_dir)
    
    if not archive_path.exists():
        return []
    
    archives = []
    for archive_subdir in sorted(archive_path.iterdir(), reverse=True):
        if archive_subdir.is_dir() and archive_subdir.name.startswith('archive_'):
            file_count = len(list(archive_subdir.glob('*.png')))
            timestamp_str = archive_subdir.name.replace('archive_', '')
            
            # Parse timestamp for display
            try:
                dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                display_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                display_time = timestamp_str
            
            archives.append((archive_subdir.name, file_count, display_time))
    
    return archives


def print_archive_summary(archive_dir):
    """Print a summary of all archives"""
    archives = list_archives(archive_dir)
    
    if not archives:
        print("No archives found.")
        return
    
    print("\nAvailable Archives:")
    print("-" * 70)
    print(f"{'Archive Name':<30} {'Files':<10} {'Created':<30}")
    print("-" * 70)
    
    for name, count, timestamp in archives:
        print(f"{name:<30} {count:<10} {timestamp:<30}")
    
    print("-" * 70)
    print(f"Total archives: {len(archives)}")
