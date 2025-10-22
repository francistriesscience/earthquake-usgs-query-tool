import json
import os
from datetime import datetime


def save_data(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if isinstance(data, dict):
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
    else:
        with open(output_file, 'w') as f:
            f.write(data)

    print(f"Data saved to {output_file}")


def generate_filename(params):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    parts = []
    if 'starttime' in params:
        parts.append(f"start_{params['starttime'].replace('-', '').replace(':', '').replace('T', '_')}")
    if 'endtime' in params:
        parts.append(f"end_{params['endtime'].replace('-', '').replace(':', '').replace('T', '_')}")
    if 'minmagnitude' in params:
        parts.append(f"minmag_{params['minmagnitude']}")

    filename = f"earthquakes_{'_'.join(parts)}_{timestamp}.{params.get('format', 'geojson')}"
    return os.path.join("dataset", "raw", filename)