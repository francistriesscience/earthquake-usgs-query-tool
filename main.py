#!/usr/bin/env python3

from lib.constants import BASE_URL
from src.api import query_earthquakes, create_session
from src.params import build_query_params
from src.file_utils import save_data, generate_filename
from src.cli import parse_args
from src.monthly import query_monthly_earthquakes


def main():
    args = parse_args()

    # Handle monthly query mode
    if args.monthly:
        # Use provided starttime and endtime, or defaults
        start_date = args.starttime 
        end_date = args.endtime
        
        session = create_session()
        try:
            print(f"Starting monthly earthquake queries from {start_date} to {end_date}...")
            query_monthly_earthquakes(BASE_URL, start_date, end_date, session=session)
            print('Monthly queries completed successfully!')
        except Exception as e:
            print(f'Error: {e}')
            exit(1)
        return

    # Regular single query mode
    # Create session for API calls
    session = create_session()

    # Build query parameters
    params = build_query_params(args)

    # Query the API
    data = query_earthquakes(BASE_URL, params, session)

    # Determine output file
    output_file = args.output or generate_filename(params)

    # Save the data
    save_data(data, output_file)


if __name__ == "__main__":
    main()
