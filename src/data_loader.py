import fastf1
import pandas as pd
import os

# enable FastF1 cache
fastf1.Cache.enable_cache("data/raw")


def load_race_results(year, race_name):
    """
    Load race results for a given race.
    """

    print(f"Downloading {year} {race_name}")

    session = fastf1.get_session(year, race_name, 'R')
    session.load()

    results = session.results[[
        'Abbreviation',
        'DriverNumber',
        'TeamName',
        'Position',
        'GridPosition',
        'Points'
    ]]

    results["Year"] = year
    results["Race"] = race_name

    return results


def save_race_results(year, race_name):
    """
    Save race results to CSV
    """

    os.makedirs("data/raw", exist_ok=True)

    df = load_race_results(year, race_name)

    race_clean = race_name.replace(" ", "_")

    file_path = f"data/raw/{year}_{race_clean}_results.csv"

    df.to_csv(file_path, index=False)

    print(f"Saved {file_path}")


def download_season(year):
    """
    Download all races for a given year automatically.
    """

    print(f"\nDownloading season {year}")

    schedule = fastf1.get_event_schedule(year)

    races = schedule[schedule['EventFormat'] == 'conventional']

    for _, race in races.iterrows():

        race_name = race['EventName']

        try:
            save_race_results(year, race_name)

        except Exception as e:
            print(f"Skipped {race_name} ({e})")


def download_multiple_seasons(start_year, end_year):
    """
    Download multiple seasons.
    """

    for year in range(start_year, end_year + 1):

        download_season(year)


if __name__ == "__main__":

    # Download historical seasons
    download_multiple_seasons(2018, 2025)