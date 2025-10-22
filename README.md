# Earthquake USGS Query Tool

A comprehensive Python tool for querying and retrieving earthquake data from the USGS Earthquake Catalog API. Supports both single queries and batch monthly downloads with flexible filtering options.

## Features

- **Complete USGS API Support**: All parameters from the FDSN Event Web Service
- **Multiple Output Formats**: GeoJSON, CSV, XML, KML, and text
- **Monthly Batch Processing**: Automatically break date ranges into monthly queries
- **Flexible Filtering**: Time, location (rectangle/circle), magnitude, depth, and more
- **Makefile Automation**: Predefined queries and custom argument support
- **Modular Architecture**: Clean separation of concerns with reusable components

## Project Structure

```
earthquake-usgs-query-tool/
├── main.py                 # Main entry point
├── monthly_query.py        # Legacy monthly query script (deprecated)
├── requirements.txt         # Python dependencies
├── Makefile                # Build automation and query shortcuts
├── .env                    # Environment variables (API base URL)
├── .gitignore             # Git ignore rules
├── .vscode/               # VS Code configuration
│   └── settings.json
├── lib/                   # Library modules
│   ├── __init__.py
│   └── constants.py       # API constants and environment loading
├── src/                   # Core functionality modules
│   ├── __init__.py
│   ├── api.py             # API querying functions
│   ├── cli.py             # Command-line argument parsing
│   ├── params.py          # Parameter building utilities
│   ├── file_utils.py      # File saving and naming utilities
│   └── monthly.py         # Monthly batch query functionality
└── dataset/               # Output directory
    └── raw/               # Raw data files (auto-generated)
```

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

3. **Verify installation:**
   ```bash
   python main.py --help
   ```

## Usage

### Makefile Targets (Recommended)

The easiest way to use the tool is through predefined Makefile targets:

```bash
# Install dependencies
make install

# Predefined regional queries
make query-california     # California earthquakes (mag ≥ 3.0)
make query-japan          # Japan region earthquakes
make query-alaska         # Alaska region earthquakes
make query-pacific-ring   # Pacific Ring of Fire

# Predefined magnitude/depth queries
make query-significant    # Significant worldwide (mag ≥ 6.0)
make query-depth-shallow  # Shallow earthquakes (depth ≤ 50km)
make query-depth-deep     # Deep earthquakes (depth ≥ 300km)

# Time-based queries
make query-worldwide      # Last 30 days worldwide
make query-recent         # Last 7 days (mag ≥ 4.0)

# Custom queries with flexible arguments
make query-custom ARGS='--starttime 2024-01-01 --minmagnitude 5.0'
make query-custom ARGS='--latitude 37.7749 --longitude -122.4194 --maxradiuskm 100'

# Monthly batch queries (downloads month-by-month as CSV files)
make query-custom ARGS='--starttime 2001-01-01 --endtime 2025-10-22 --monthly'
make query-custom ARGS='--starttime 2020-01-01 --endtime 2023-12-31 --monthly --minmagnitude 4.0'

# Clean up generated data
make clean
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

The `--monthly` flag enables automatic batch processing of large date ranges:

### How It Works
1. Takes your `--starttime` and `--endtime` parameters
2. Breaks the range into monthly chunks (e.g., 2024-01-01 to 2024-01-31, 2024-02-01 to 2024-02-29, etc.)
3. Queries each month separately as CSV files
4. Saves files as `YYYYMMDD.csv` in `dataset/raw/`

### Examples

```bash
# Download all earthquakes from 2001-2025, month by month
python main.py --starttime 2001-01-01 --endtime 2025-10-22 --monthly

# Monthly queries with magnitude filter
python main.py --starttime 2020-01-01 --endtime 2023-12-31 --minmagnitude 4.0 --monthly

# Monthly queries in specific region
python main.py --starttime 2010-01-01 --endtime 2020-12-31 --minlatitude 30 --maxlatitude 46 --minlongitude 128 --maxlongitude 146 --monthly
```

### Output Files
```
dataset/raw/
├── 20010101.csv    # January 2001
├── 20010201.csv    # February 2001
├── 20010301.csv    # March 2001
└── ...             # Continues monthly
```

## Output Formats

### GeoJSON (Default)
- Feature collection with earthquake properties
- Includes geometry, magnitude, time, depth, etc.
- Best for programmatic processing

### CSV
- Tabular format with headers
- Includes all available earthquake data
- Best for spreadsheet analysis

### XML/QuakeML
- Standard earthquake data format
- Detailed event information
- Best for scientific applications

### KML
- Google Earth compatible
- Geographic visualization
- Includes time animations

## Configuration

### Environment Variables (.env)
```bash
BASE_URL=https://earthquake.usgs.gov/fdsnws/event/1/query
```

### VS Code Settings (.vscode/settings.json)
- Hides Python cache files and build artifacts
- Hides generated data files in `dataset/raw/`
- Keeps important project files visible

## Examples

### Basic Queries

```bash
# Recent significant earthquakes
python main.py --starttime 2024-01-01 --minmagnitude 6.0 --orderby magnitude

# California earthquakes this year
python main.py --starttime 2024-01-01 --minlatitude 32 --maxlatitude 42 --minlongitude -125 --maxlongitude -114 --minmagnitude 3.0

# Circle search around San Francisco
python main.py --latitude 37.7749 --longitude -122.4194 --maxradiuskm 100 --starttime 2024-01-01
```

### Advanced Queries

```bash
# Deep earthquakes in subduction zones
python main.py --mindepth 300 --minlatitude -60 --maxlatitude 60 --minlongitude 140 --maxlongitude -120 --minmagnitude 5.0

# Reviewed events only
python main.py --starttime 2024-01-01 --reviewstatus reviewed --minmagnitude 4.0

# Events with PAGER alerts
python main.py --starttime 2024-01-01 --alertlevel orange --orderby magnitude
```

### Batch Processing

```bash
# Historical data collection
python main.py --starttime 2000-01-01 --endtime 2024-12-31 --monthly --format csv

# Regional historical analysis
python main.py --starttime 2010-01-01 --endtime 2020-12-31 --minlatitude 20 --maxlatitude 50 --minlongitude -130 --maxlongitude -110 --monthly
```

## Development

### Architecture

The codebase follows a modular architecture:

- **`main.py`**: Entry point and orchestration
- **`src/api.py`**: HTTP requests and API communication
- **`src/cli.py`**: Command-line interface parsing
- **`src/params.py`**: Parameter validation and building
- **`src/file_utils.py`**: File operations and naming
- **`src/monthly.py`**: Date range processing for batch queries
- **`lib/constants.py`**: Configuration and environment handling

### Adding New Features

1. Add new parameters to `src/cli.py`
2. Implement parameter handling in `src/params.py`
3. Add API logic to `src/api.py` if needed
4. Update `main.py` for new functionality
5. Add Makefile targets for common use cases

### Testing

```bash
# Test individual components
python -c "from src.monthly import generate_monthly_date_ranges; print(generate_monthly_date_ranges('2024-01-01', '2024-03-01'))"

# Test API connectivity
python main.py --starttime 2024-01-01 --endtime 2024-01-02 --limit 1
```

## API Reference

This tool implements the [USGS FDSN Event Web Service Specification](https://earthquake.usgs.gov/fdsnws/event/1/). For complete API documentation, visit:

- [USGS Earthquake Catalog API](https://earthquake.usgs.gov/fdsnws/event/1/)
- [Real-time GeoJSON Feeds](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## License

See LICENSE file for details.

## Disclaimer

This tool queries public data from the USGS Earthquake Hazards Program. Please respect API usage guidelines and consider using Real-time GeoJSON Feeds for high-frequency applications.
