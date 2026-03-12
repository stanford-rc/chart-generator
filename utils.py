"""
Utility functions for data processing and color calculations
"""

def read_data(filename):
    """Read and parse the data file"""
    departments = []
    counts = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(maxsplit=1)
                count = int(parts[0])
                department = parts[1] if len(parts) > 1 else 'Unknown'
                counts.append(count)
                departments.append(department)
    
    return departments, counts

def get_text_color(hex_color):
    """
    Determine if white or black text should be used based on background color.
    Uses relative luminance calculation for accessibility (WCAG standard).
    """
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Convert to RGB
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Calculate relative luminance
    def get_channel_luminance(c):
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4
    
    r_lum = get_channel_luminance(r)
    g_lum = get_channel_luminance(g)
    b_lum = get_channel_luminance(b)
    
    luminance = 0.2126 * r_lum + 0.7152 * g_lum + 0.0722 * b_lum
    
    # Return white for dark backgrounds, black for light backgrounds
    return 'white' if luminance < 0.5 else 'black'

def print_summary(departments, counts, label="Data"):
    """Print data summary to console"""
    total = sum(counts)
    print(f"\n{label} Summary:")
    print("-" * 70)
    print(f"{'Rank':<6} {'Department/School':<50} {'Count':<8} {'%':<6}")
    print("-" * 70)
    for i, (dept, count) in enumerate(sorted(zip(departments, counts), 
                                             key=lambda x: x[1], reverse=True), 1):
        percentage = (count / total) * 100
        print(f"{i:<6} {dept:<50} {count:<8} {percentage:>5.1f}%")
    print("-" * 70)
    print(f"{'':6} {'TOTAL':<50} {total:<8} {'100.0%':>6}")
    print("-" * 70)
