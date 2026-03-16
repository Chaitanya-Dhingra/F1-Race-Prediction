import pandas as pd
import os

DATA_PATH = "data/raw"

K = 20
INITIAL_RATING = 1500

TEAM_WEIGHT = 1.5   # Option B


def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def update_rating(rating, expected, actual):
    return rating + K * (actual - expected)


def load_all_races():
    files = [f for f in os.listdir(DATA_PATH) if f.endswith(".csv")]

    dfs = []

    for file in files:
        df = pd.read_csv(os.path.join(DATA_PATH, file))
        dfs.append(df)

    data = pd.concat(dfs, ignore_index=True)

    return data


def train_ratings():

    data = load_all_races()

    driver_ratings = {}
    team_ratings = {}

    races = data.groupby(["Year", "Race"])

    for _, race in races:

        race = race.sort_values("Position")

        drivers = race.to_dict("records")

        for i in range(len(drivers)):
            for j in range(i + 1, len(drivers)):

                d1 = drivers[i]
                d2 = drivers[j]

                driver1 = d1["Abbreviation"]
                driver2 = d2["Abbreviation"]

                team1 = d1["TeamName"]
                team2 = d2["TeamName"]

                driver_ratings.setdefault(driver1, INITIAL_RATING)
                driver_ratings.setdefault(driver2, INITIAL_RATING)

                team_ratings.setdefault(team1, INITIAL_RATING)
                team_ratings.setdefault(team2, INITIAL_RATING)

                # PERFORMANCE RATING (Option B)
                rating1 = driver_ratings[driver1] + TEAM_WEIGHT * team_ratings[team1]
                rating2 = driver_ratings[driver2] + TEAM_WEIGHT * team_ratings[team2]

                expected1 = expected_score(rating1, rating2)
                expected2 = expected_score(rating2, rating1)

                actual1 = 1
                actual2 = 0

                # Update driver ratings
                driver_ratings[driver1] = update_rating(driver_ratings[driver1], expected1, actual1)
                driver_ratings[driver2] = update_rating(driver_ratings[driver2], expected2, actual2)

                # Update team ratings
                team_ratings[team1] = update_rating(team_ratings[team1], expected1, actual1)
                team_ratings[team2] = update_rating(team_ratings[team2], expected2, actual2)

    return driver_ratings, team_ratings


if __name__ == "__main__":

    driver_ratings, team_ratings = train_ratings()

    driver_df = pd.DataFrame(driver_ratings.items(), columns=["Driver", "Rating"])
    team_df = pd.DataFrame(team_ratings.items(), columns=["Team", "Rating"])

    driver_df.to_csv("data/processed/driver_ratings.csv", index=False)
    team_df.to_csv("data/processed/team_ratings.csv", index=False)

    print("Ratings saved.")