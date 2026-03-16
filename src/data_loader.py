import fastf1
import pandas as pd
import os

# enable FastF1 caching
fastf1.Cache.enable_cache("data/raw")


def load_race_results(year, race_name):
    """
    Load race results for a given race.
    """
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
    Save race results to CSV.
    """
    df = load_race_results(year, race_name)

    file_path = f"data/raw/{year}_{race_name}_results.csv"
    df.to_csv(file_path, index=False)

    print(f"Saved {file_path}")


if __name__ == "__main__":

    races = [
        (2023, "Bahrain"),
        (2023, "Saudi Arabian"),
        (2023, "Australian"),
        (2023, "Azerbaijan"),
        (2023, "Miami"),
        (2023, "Monaco"),
        (2023, "Spanish"),
        (2023, "Canadian"),
        (2023, "British"),
        (2023, "Hungarian"),
        (2023, "Belgian"),
        (2023, "Dutch"),
        (2023, "Italian")
    ]

    for year, race in races:
        save_race_results(year, race)