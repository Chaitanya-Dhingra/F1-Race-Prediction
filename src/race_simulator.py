import pandas as pd
import numpy as np
import os

TEAM_WEIGHT = 1.5
GRID_WEIGHT = 30
NOISE_STD = 80

SIMULATIONS = 10000


def load_ratings():

    driver_df = pd.read_csv("data/processed/driver_ratings.csv")
    team_df = pd.read_csv("data/processed/team_ratings.csv")

    driver_ratings = dict(zip(driver_df.Driver, driver_df.Rating))
    team_ratings = dict(zip(team_df.Team, team_df.Rating))

    return driver_ratings, team_ratings


def load_latest_grid():

    files = [f for f in os.listdir("data/raw") if f.endswith(".csv")]

    latest = sorted(files)[-1]

    df = pd.read_csv(os.path.join("data/raw", latest))

    grid = dict(zip(df.Abbreviation, df.GridPosition))
    teams = dict(zip(df.Abbreviation, df.TeamName))

    return grid, teams


def simulate_race(driver_ratings, team_ratings, grid_positions, driver_teams):

    performances = []

    max_grid = max(grid_positions.values())

    for driver in grid_positions:

        team = driver_teams.get(driver)

        # skip drivers not present in latest race
        if team is None:
            continue

        grid_pos = grid_positions.get(driver, max_grid)

        grid_advantage = max_grid - grid_pos

        base_strength = (
        driver_ratings[driver]
        + TEAM_WEIGHT * team_ratings.get(team, 1500)
        + GRID_WEIGHT * grid_advantage
        )

        noise = np.random.normal(0, NOISE_STD)

        performance = base_strength + noise

        performances.append((driver, performance))

    performances.sort(key=lambda x: x[1], reverse=True)

    return [d[0] for d in performances]


def monte_carlo_simulation():

    driver_ratings, team_ratings = load_ratings()

    grid_positions, driver_teams = load_latest_grid()

    drivers = list(driver_ratings.keys())

    win_counts = {d: 0 for d in drivers}
    podium_counts = {d: 0 for d in drivers}
    top5_counts = {d: 0 for d in drivers}
    total_positions = {d: 0 for d in drivers}

    for _ in range(SIMULATIONS):

        result = simulate_race(
            driver_ratings,
            team_ratings,
            grid_positions,
            driver_teams
        )

        for pos, driver in enumerate(result):

            if pos == 0:
                win_counts[driver] += 1

            if pos < 3:
                podium_counts[driver] += 1

            if pos < 5:
                top5_counts[driver] += 1

            total_positions[driver] += pos + 1

    stats = []

    for driver in drivers:

        stats.append({
            "Driver": driver,
            "Win %": win_counts[driver] / SIMULATIONS * 100,
            "Podium %": podium_counts[driver] / SIMULATIONS * 100,
            "Top 5 %": top5_counts[driver] / SIMULATIONS * 100,
            "Avg Finish": total_positions[driver] / SIMULATIONS
        })

    results_df = pd.DataFrame(stats)

    results_df = results_df.sort_values("Win %", ascending=False)

    return results_df


if __name__ == "__main__":

    results = monte_carlo_simulation()

    print("\nRace Outcome Probabilities\n")

    print(results.to_string(index=False))

    os.makedirs("results", exist_ok=True)

    results.to_csv("results/race_probabilities.csv", index=False)

    print("\nSaved results to results/race_probabilities.csv")