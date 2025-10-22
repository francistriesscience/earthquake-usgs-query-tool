import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from .api import query_earthquakes, create_session
from .params import build_query_params
from .file_utils import save_data


def generate_monthly_date_ranges(start_date, end_date):
    ranges = []
    current = datetime.fromisoformat(start_date)

    while current < datetime.fromisoformat(end_date):
        month_start = current.replace(day=1)
        month_end = month_start + relativedelta(months=1) - timedelta(days=1)

        # Don't go beyond the end date
        if month_end > datetime.fromisoformat(end_date):
            month_end = datetime.fromisoformat(end_date)

        ranges.append((month_start.date().isoformat(), month_end.date().isoformat()))
        current = month_start + relativedelta(months=1)

    return ranges


def query_monthly_earthquakes(base_url, start_date, end_date, additional_params=None, session=None):
    if session is None:
        session = create_session()

    if additional_params is None:
        additional_params = {}

    # Force CSV format for monthly queries
    params_template = {'format': 'csv', **additional_params}

    date_ranges = generate_monthly_date_ranges(start_date, end_date)

    for month_start, month_end in date_ranges:
        # Create params for this month
        month_params = {
            **params_template,
            'starttime': month_start,
            'endtime': month_end
        }

        print(f"Querying month: {month_start} to {month_end}")

        # Query the API
        data = query_earthquakes(base_url, month_params, session)

        # Generate filename (YYYYMMDD.csv)
        filename_date = month_start.replace('-', '')
        filename = f"{filename_date}.csv"
        output_file = os.path.join("dataset", "raw", filename)

        # Save the data
        save_data(data, output_file)