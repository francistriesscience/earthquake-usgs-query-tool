import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

from .api import query_earthquakes, create_session, QueryLimitExceededError
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


def query_monthly_earthquakes(
    base_url, start_date, end_date, additional_params=None, session=None
):
    if session is None:
        session = create_session()

    if additional_params is None:
        additional_params = {}

    # Force CSV format for monthly queries
    params_template = {"format": "csv", **additional_params}

    date_ranges = generate_monthly_date_ranges(start_date, end_date)

    print(
        f"Starting monthly queries from {start_date} to {end_date} ({len(date_ranges)} months)"
    )

    # Use progress bar for monthly queries
    with tqdm(
        total=len(date_ranges), desc="Querying months", unit="month", ncols=80
    ) as pbar:
        for month_start, month_end in date_ranges:
            # Create params for this month
            month_params = {
                **params_template,
                "starttime": month_start,
                "endtime": month_end,
            }

            # Update progress bar description with current month
            pbar.set_description(f"Querying {month_start[:7]}")

            # Try to query the API
            try:
                data = query_earthquakes(base_url, month_params, session)
            except QueryLimitExceededError:
                tqdm.write(
                    f"\nQuery limit exceeded for {month_start} to {month_end}. Splitting into two halves..."
                )
                # Split the month into two halves
                start_dt = datetime.fromisoformat(month_start)
                end_dt = datetime.fromisoformat(month_end)
                mid_dt = start_dt + (end_dt - start_dt) // 2
                mid_date = mid_dt.date().isoformat()

                # First half: month_start to mid_date
                tqdm.write(f"Querying first half: {month_start} to {mid_date}")
                first_params = {
                    **month_params,
                    "starttime": month_start,
                    "endtime": mid_date,
                }
                first_data = query_earthquakes(base_url, first_params, session)

                # Second half: mid_date + 1 day to month_end
                next_day = (mid_dt + timedelta(days=1)).date().isoformat()
                tqdm.write(f"Querying second half: {next_day} to {month_end}")
                second_params = {
                    **month_params,
                    "starttime": next_day,
                    "endtime": month_end,
                }
                second_data = query_earthquakes(base_url, second_params, session)

                # Combine CSV data: first_data + second_data without header
                first_lines = first_data.split("\n")
                second_lines = second_data.split("\n")
                if second_lines:  # Skip header for second part
                    combined_lines = first_lines + second_lines[1:]
                else:
                    combined_lines = first_lines
                data = "\n".join(combined_lines)

            # Generate filename (YYYYMMDD.csv)
            filename_date = month_start.replace("-", "")
            filename = f"{filename_date}.csv"
            output_file = os.path.join("dataset", "raw", filename)

            # Save the data
            save_data(data, output_file)

            # Update progress bar
            pbar.update(1)

    tqdm.write("Monthly queries completed!")
