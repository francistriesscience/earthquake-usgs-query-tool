# Earthquake USGS Query Tool

A comprehensive Python tool for querying and retrieving earthquake data from the USGS Earthquake Catalog API. Supports both single queries and batch monthly downloads with flexible filtering options.

## Features

- **Complete USGS API Support**: All parameters from the FDSN Event Web Service
- **Multiple Output Formats**: GeoJSON, CSV, XML, KML, and text
- **Monthly Batch Processing**: Automatically break date ranges into monthly queries with automatic retry on API limits
- **Progress Bars**: Visual progress indicators for long-running queries using tqdm
- **Flexible Filtering**: Time, location (rectangle/circle), magnitude, depth, and more
- **Shell Script Interface**: Simple command-line interface with direct argument passing
- **Modular Architecture**: Clean separation of concerns with reusable components

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/francistriesscience/earthquake-usgs-query-tool.git
   cd earthquake-usgs-query-tool
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make the query script executable:**
   ```bash
   chmod +x scripts/query.sh
   ```

4. **Verify installation:**
   ```bash
   python main.py --help
   ./scripts/query.sh help
   ```

## Usage

### Shell Script Commands (Recommended)

The easiest way to use the tool is through the shell script interface:

```bash
# Install dependencies
./scripts/query.sh install

# Predefined regional queries
./scripts/query.sh query-japan          # Japan region earthquakes
./scripts/query.sh query-alaska         # Alaska region earthquakes
./scripts/query.sh query-pacific-ring   # Pacific Ring of Fire

# Predefined magnitude/depth queries
./scripts/query.sh query-significant    # Significant worldwide (mag ≥ 6.0)
./scripts/query.sh query-depth-shallow  # Shallow earthquakes (depth ≤ 50km)
./scripts/query.sh query-depth-deep     # Deep earthquakes (depth ≥ 300km)

# Time-based queries
./scripts/query.sh query-worldwide      # Last 30 days worldwide
./scripts/query.sh query-recent         # Last 7 days (mag ≥ 4.0)

# Custom queries with flexible arguments
./scripts/query.sh query-custom --starttime 2024-01-01 --minmagnitude 5.0
./scripts/query.sh query-custom --latitude 37.7749 --longitude -122.4194 --maxradiuskm 100

# Monthly batch queries (downloads month-by-month as CSV files)
./scripts/query.sh query-custom --starttime 2001-01-01 --endtime 2025-10-22 --monthly
./scripts/query.sh query-custom --starttime 2020-01-01 --endtime 2023-12-31 --monthly --minmagnitude 4.0

# Clean up generated data
./scripts/query.sh clean

# Show help
./scripts/query.sh help
```

### Direct Python Usage

You can also run the script directly with command-line arguments:

```bash
# Basic query
python main.py --starttime 2024-01-01 --endtime 2024-01-31 --minmagnitude 4.0

# Monthly batch processing
python main.py --starttime 2001-01-01 --endtime 2025-10-22 --monthly

# Advanced filtering
python main.py --minlatitude 32 --maxlatitude 42 --minlongitude -125 --maxlongitude -114 --minmagnitude 3.0 --format csv
```

## API Parameters

The tool supports all parameters from the USGS Earthquake Catalog API:

### Time Parameters
- `--starttime` - Start time (ISO8601 format, e.g., 2024-01-01)
- `--endtime` - End time (ISO8601 format, e.g., 2024-12-31)
- `--updatedafter` - Updated after time (ISO8601 format)

### Location Parameters (Rectangle)
- `--minlatitude`, `--maxlatitude` - Latitude bounds (-90 to 90)
- `--minlongitude`, `--maxlongitude` - Longitude bounds (-180 to 180)

### Location Parameters (Circle)
- `--latitude`, `--longitude` - Circle center coordinates
- `--maxradius` - Maximum radius in degrees (0-180)
- `--maxradiuskm` - Maximum radius in kilometers (0-20001.6)

### Magnitude & Depth
- `--minmagnitude` - Minimum magnitude
- `--maxmagnitude` - Maximum magnitude
- `--mindepth` - Minimum depth in km (-100 to 1000)
- `--maxdepth` - Maximum depth in km (-100 to 1000)

### Data Source & Event Filters
- `--catalog` - Limit to specific catalog
- `--contributor` - Limit to specific contributor
- `--eventid` - Query specific event by ID
- `--eventtype` - Limit to event type (e.g., earthquake)

### Output & Performance
- `--format` - Output format: geojson, csv, xml, kml, text, quakeml
- `--orderby` - Sort order: time, time-asc, magnitude, magnitude-asc
- `--limit` - Maximum number of results (1-20000)
- `--offset` - Results offset for pagination

### Advanced Filters
- `--includeallmagnitudes` - Include all magnitudes for each event
- `--includeallorigins` - Include all origins for each event
- `--includearrivals` - Include phase arrivals
- `--includedeleted` - Include deleted events (true/only)
- `--includesuperseded` - Include superseded events
- `--alertlevel` - PAGER alert level (green/yellow/orange/red)
- `--reviewstatus` - Review status (automatic/reviewed)

### Special Modes
- `--monthly` - Enable monthly batch processing (breaks date range into monthly queries)
- `--output` - Custom output file path (default: auto-generated)

## Monthly Batch Processing

The `--monthly` flag enables automatic batch processing of large date ranges with built-in retry logic for API limits:

### How It Works
1. Takes your `--starttime` and `--endtime` parameters
2. Breaks the range into monthly chunks (e.g., 2024-01-01 to 2024-01-31, 2024-02-01 to 2024-02-29, etc.)
3. Queries each month separately as CSV files
4. **Automatic Retry**: If a month exceeds 20,000 results (USGS API limit), automatically splits that month into two halves and combines the results
5. **Progress Tracking**: Shows real-time progress bars indicating completion status and current month being processed
6. Saves files as `YYYYMMDD.csv` in `dataset/raw/`

### Examples

```bash
# Download all earthquakes from 2001-2025, month by month
./scripts/query.sh query-custom --starttime 2001-01-01 --endtime 2025-10-22 --monthly

# Monthly queries with magnitude filter
./scripts/query.sh query-custom --starttime 2020-01-01 --endtime 2023-12-31 --minmagnitude 4.0 --monthly

# Monthly queries in specific region
./scripts/query.sh query-custom --starttime 2010-01-01 --endtime 2020-12-31 --minlatitude 30 --maxlatitude 46 --minlongitude 128 --maxlongitude 146 --monthly
```

### Output Files
```
dataset/raw/
├── 20010101.csv    # January 2001
├── 20010201.csv    # February 2001
├── 20010301.csv    # March 2001
└── ...             # Continues monthly
```

## Disclaimer

This tool queries public data from the USGS Earthquake Hazards Program. Please respect API usage guidelines and consider using Real-time GeoJSON Feeds for high-frequency applications.
