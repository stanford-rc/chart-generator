#!/usr/bin/env python3
"""
Test script to verify Source Sans font loads correctly
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

FONT_PATH = '/projects/bprogers/main/saracook/.fonts/Source_Sans_3/SourceSans3-VariableFont_wght.ttf'

def test_font():
    print(f"Testing font: {FONT_PATH}")
    print(f"File exists: {os.path.exists(FONT_PATH)}")
    
    if os.path.exists(FONT_PATH):
        try:
            # Add the font
            fm.fontManager.addfont(FONT_PATH)
            prop = fm.FontProperties(fname=FONT_PATH)
            font_name = prop.get_name()
            
            print(f"✓ Font loaded successfully: {font_name}")
            
            # Create a test chart
            fig, ax = plt.subplots(figsize=(8, 6))
            
            # Set font
            plt.rcParams['font.family'] = font_name
            
            # Create simple test
            ax.text(0.5, 0.5, f'Source Sans 3 Font Test\n{font_name}', 
                   ha='center', va='center', fontsize=24, weight='bold')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            plt.tight_layout()
            plt.savefig('font_test.png', dpi=150)
            print("✓ Test chart saved as 'font_test.png'")
            
        except Exception as e:
            print(f"✗ Error loading font: {e}")
    else:
        print(f"✗ Font file not found")

if __name__ == '__main__':
    test_font()
