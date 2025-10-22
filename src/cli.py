import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="Query USGS Earthquake Catalog API")

    # Monthly query mode
    parser.add_argument('--monthly', action='store_true',
                       help='Run monthly queries from 2001-01-01 to 2025-10-22 (saves as CSV)')

    # Format
    parser.add_argument('--format', choices=['geojson', 'csv', 'kml', 'text', 'xml', 'quakeml'],
                       default='geojson', help='Output format (default: geojson)')

    # Time
    parser.add_argument('--starttime', help='Start time (ISO8601 format)')
    parser.add_argument('--endtime', help='End time (ISO8601 format)')
    parser.add_argument('--updatedafter', help='Updated after time (ISO8601 format)')

    # Location - Rectangle
    parser.add_argument('--minlatitude', type=float, help='Minimum latitude')
    parser.add_argument('--maxlatitude', type=float, help='Maximum latitude')
    parser.add_argument('--minlongitude', type=float, help='Minimum longitude')
    parser.add_argument('--maxlongitude', type=float, help='Maximum longitude')

    # Location - Circle
    parser.add_argument('--latitude', type=float, help='Latitude for circle search')
    parser.add_argument('--longitude', type=float, help='Longitude for circle search')
    parser.add_argument('--maxradius', type=float, help='Maximum radius in degrees')
    parser.add_argument('--maxradiuskm', type=float, help='Maximum radius in kilometers')

    # Other
    parser.add_argument('--catalog', help='Catalog')
    parser.add_argument('--contributor', help='Contributor')
    parser.add_argument('--eventid', help='Event ID')
    parser.add_argument('--includeallmagnitudes', action='store_true', help='Include all magnitudes')
    parser.add_argument('--includeallorigins', action='store_true', help='Include all origins')
    parser.add_argument('--includearrivals', action='store_true', help='Include arrivals')
    parser.add_argument('--includedeleted', choices=['true', 'only'], help='Include deleted events')
    parser.add_argument('--includesuperseded', action='store_true', help='Include superseded')
    parser.add_argument('--limit', type=int, help='Limit number of results')
    parser.add_argument('--maxdepth', type=float, help='Maximum depth')
    parser.add_argument('--maxmagnitude', type=float, help='Maximum magnitude')
    parser.add_argument('--mindepth', type=float, help='Minimum depth')
    parser.add_argument('--minmagnitude', type=float, help='Minimum magnitude')
    parser.add_argument('--offset', type=int, help='Offset for results')
    parser.add_argument('--orderby', choices=['time', 'time-asc', 'magnitude', 'magnitude-asc'],
                       default='time', help='Order by')

    # Extensions
    parser.add_argument('--alertlevel', choices=['green', 'yellow', 'orange', 'red'], help='Alert level')
    parser.add_argument('--callback', help='JSONP callback')
    parser.add_argument('--eventtype', help='Event type')
    parser.add_argument('--jsonerror', action='store_true', help='JSON error format')
    parser.add_argument('--kmlanimated', action='store_true', help='KML animated')
    parser.add_argument('--kmlcolorby', choices=['age', 'depth'], help='KML color by')
    parser.add_argument('--maxcdi', type=float, help='Maximum CDI')
    parser.add_argument('--maxgap', type=float, help='Maximum gap')
    parser.add_argument('--maxmmi', type=float, help='Maximum MMI')
    parser.add_argument('--maxsig', type=int, help='Maximum significance')
    parser.add_argument('--mincdi', type=float, help='Minimum CDI')
    parser.add_argument('--minfelt', type=int, help='Minimum felt')
    parser.add_argument('--mingap', type=float, help='Minimum gap')
    parser.add_argument('--minsig', type=int, help='Minimum significance')
    parser.add_argument('--nodata', type=int, choices=[204, 404], help='No data error code')
    parser.add_argument('--producttype', help='Product type')
    parser.add_argument('--productcode', help='Product code')
    parser.add_argument('--reviewstatus', choices=['automatic', 'reviewed'], help='Review status')

    # Output
    parser.add_argument('--output', help='Output file path (default: auto-generated)')

    return parser


def parse_args():
    """Parse command line arguments."""
    parser = create_parser()
    return parser.parse_args()