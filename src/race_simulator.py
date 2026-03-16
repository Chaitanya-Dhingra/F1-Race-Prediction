import pandas as pd
import numpy as np
import random

TEAM_WEIGHT = 1.5
NOISE_STD = 80

SIMULATIONS = 10000


def load_ratings():

    driver_df = pd.read_csv("data/processed/driver_ratings.csv")
    team_df = pd.read_csv("data/processed/team_ratings.csv")

    driver_ratings = dict(zip(driver_df.Driver, driver_df.Rating))
    team_ratings = dict(zip(team_df.Team, team_df.Rating))

    return driver_ratings, team_ratings


def simulate_race(driver_ratings, team_ratings):

    drivers = list(driver_ratings.keys())

    performances = []

    for driver in drivers:

        team = None

        for t in team_ratings:
            # this part will later be improved
            team = t

        base = driver_ratings[driver] + TEAM_WEIGHT * team_ratings[team]

        noise = np.random.normal(0, NOISE_STD)

        performance = base + noise

        performances.append((driver, performance))

    performances.sort(key=lambda x: x[1], reverse=True)

    return [d[0] for d in performances]


def monte_carlo_simulation():

    driver_ratings, team_ratings = load_ratings()

    win_counts = {d: 0 for d in driver_ratings}

    for _ in range(SIMULATIONS):

        result = simulate_race(driver_ratings, team_ratings)

        winner = result[0]

        win_counts[winner] += 1

    probabilities = {
        d: win_counts[d] / SIMULATIONS
        for d in win_counts
    }

    return probabilities


if __name__ == "__main__":

    probs = monte_carlo_simulation()

    for driver, p in sorted(probs.items(), key=lambda x: x[1], reverse=True):
        print(driver, round(p * 100, 2), "% win chance")