#!/usr/bin/env python3
import sys
import os

print("Current directory:", os.getcwd())
print("\nPython path:")
for p in sys.path:
    print(f"  {p}")

print("\nLooking for charts directory...")
charts_dir = os.path.join(os.getcwd(), 'charts')
print(f"Charts directory exists: {os.path.exists(charts_dir)}")
print(f"Charts directory path: {charts_dir}")

if os.path.exists(charts_dir):
    print(f"\nContents of charts/:")
    for item in os.listdir(charts_dir):
        print(f"  {item}")
    
    init_file = os.path.join(charts_dir, '__init__.py')
    print(f"\n__init__.py exists: {os.path.exists(init_file)}")
    
    if os.path.exists(init_file):
        print("\nContents of __init__.py:")
        with open(init_file, 'r') as f:
            print(f.read())

print("\n" + "="*60)
print("Attempting import...")
try:
    from charts import create_pie_chart
    print("✓ SUCCESS! Import worked.")
except ImportError as e:
    print(f"✗ FAILED: {e}")
    
    # Try alternative import
    print("\nTrying alternative import method...")
    try:
        sys.path.insert(0, os.getcwd())
        import charts
        print(f"  Charts module found at: {charts.__file__}")
        from charts import create_pie_chart
        print("✓ Alternative import worked!")
    except Exception as e2:
        print(f"✗ Alternative also failed: {e2}")
