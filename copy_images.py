import shutil
import os
from pathlib import Path

# Get the project directory
project_dir = Path(__file__).parent

# Source and destination paths
media_dir = project_dir / 'media' / 'Maveli'
static_dir = project_dir / 'static' / 'images'

# Ensure static/images exists
static_dir.mkdir(parents=True, exist_ok=True)

# Copy each image
maveli_files = ['Maveli.jpg', 'Maveli2.jpg', 'Maveli2.png', 'Maveli4.jpg']

for filename in maveli_files:
    source = media_dir / filename
    destination = static_dir / filename
    
    if source.exists():
        shutil.copy2(source, destination)
        print(f"Copied {filename}")
    else:
        print(f"Source {filename} not found")

print("Done copying Maveli images!")
