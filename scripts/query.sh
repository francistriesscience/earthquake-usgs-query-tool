#!/bin/bash

# Earthquake USGS Query Tool - Shell Script Interface
# This script provides a command-line interface to the earthquake query tool
# Usage: ./scripts/query.sh <command> [arguments]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="python3"
MAIN_SCRIPT="$PROJECT_DIR/main.py"

# Function to display help
show_help() {
    echo "Earthquake USGS Query Tool"
    echo ""
    echo "Usage: $0 <command> [arguments]"
    echo ""
    echo "Available commands:"
    echo "  help                - Show this help message"
    echo "  install             - Install Python dependencies"
    echo "  query-significant   - Query significant earthquakes worldwide (mag >= 6.0)"
    echo "  query-worldwide     - Query all earthquakes worldwide (last 30 days)"
    echo "  query-recent        - Query recent earthquakes (last 7 days, mag >= 4.0)"
    echo "  query-custom        - Run custom query with flexible arguments (supports --monthly flag)"
    echo "  query-japan         - Query earthquakes in Japan region"
    echo "  query-alaska        - Query earthquakes in Alaska region"
    echo "  query-pacific-ring  - Query earthquakes in Pacific Ring of Fire"
    echo "  query-depth-shallow - Query shallow earthquakes (depth <= 50km)"
    echo "  query-depth-deep    - Query deep earthquakes (depth >= 300km)"
    echo "  clean               - Remove generated data files"
    echo ""
    echo "Examples:"
    echo "  $0 query-custom --starttime 2024-01-01 --minmagnitude 5.0"
    echo "  $0 query-custom --starttime 2001-01-01 --endtime 2025-10-22 --monthly"
    echo "  $0 query-custom --latitude 37.7749 --longitude -122.4194 --maxradiuskm 100"
    echo "  $0 query-significant"
    echo "  $0 clean"
}

# Function to install dependencies
install_deps() {
    echo "Installing Python dependencies..."
    cd "$PROJECT_DIR"
    $PYTHON -m pip install -r requirements.txt
    echo "Installation completed."
}

# Function to run python script with arguments
run_python() {
    cd "$PROJECT_DIR"
    $PYTHON "$MAIN_SCRIPT" "$@"
}

# Main script logic
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

COMMAND="$1"
shift  # Remove the command from arguments

case "$COMMAND" in
    help|--help|-h)
        show_help
        ;;
    install)
        install_deps
        ;;
    query-significant)
        run_python --minmagnitude 6.0 --orderby magnitude --limit 100
        ;;
    query-worldwide)
        run_python --orderby time --limit 1000
        ;;
    query-recent)
        # Calculate date 7 days ago
        SEVEN_DAYS_AGO=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d '7 days ago' +%Y-%m-%d)
        run_python --starttime "$SEVEN_DAYS_AGO" --minmagnitude 4.0 --orderby time
        ;;
    query-custom)
        run_python "$@"
        ;;
    query-japan)
        run_python --minlatitude 30 --maxlatitude 46 --minlongitude 128 --maxlongitude 146 --minmagnitude 4.0 --orderby time
        ;;
    query-alaska)
        run_python --minlatitude 50 --maxlatitude 72 --minlongitude -180 --maxlongitude -130 --minmagnitude 3.0 --orderby time
        ;;
    query-pacific-ring)
        run_python --minlatitude -60 --maxlatitude 60 --minlongitude 140 --maxlongitude -120 --minmagnitude 5.0 --orderby magnitude --limit 200
        ;;
    query-depth-shallow)
        run_python --maxdepth 50 --minmagnitude 4.0 --orderby time
        ;;
    query-depth-deep)
        run_python --mindepth 300 --minmagnitude 5.0 --orderby magnitude
        ;;
    clean)
        echo "Cleaning generated data files..."
        cd "$PROJECT_DIR"
        rm -rf dataset/raw/*.json dataset/raw/*.csv dataset/raw/*.xml dataset/raw/*.kml dataset/raw/*.txt
        echo "Clean completed."
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac
