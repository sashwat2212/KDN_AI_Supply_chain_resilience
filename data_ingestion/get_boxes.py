import numpy as np
import json

# Define US bounding box
lat_min, lat_max = 24.5, 49.5   # Approximate latitude range of the US
lon_min, lon_max = -125, -66    # Approximate longitude range of the US

# Grid resolution (degrees)
lat_step = 2.5
lon_step = 2.5

# Generate grid of bounding boxes
bboxes = []
for lat in np.arange(lat_min, lat_max, lat_step):
    for lon in np.arange(lon_min, lon_max, lon_step):
        bbox = {
            "bbox": [lon, lat, lon + lon_step, lat + lat_step],
            "lat": lat + lat_step / 2,
            "lon": lon + lon_step / 2
        }
        bboxes.append(bbox)

# Save to JSON file
with open("us_grid_bboxes.json", "w") as f:
    json.dump(bboxes, f, indent=4)

print(f"Generated {len(bboxes)} bounding boxes for the US.")
