# Solution: from IDs to countries
#
# Same as f1_lap_times_countries.py, but with build_dataframe() filled in.

import random
from pathlib import Path

import pandas as pd
import seaborn as sns

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "f1db_csv"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"
YEAR = 2021  # only look at one season, so the plot stays fast and readable
NUM_RANDOM_COUNTRIES = 5
MAX_LAP_SECONDS = 150  # laps slower than this are safety-car/red-flag laps, not real pace
MIN_USABLE_LAPS = 50  # skip races (e.g. rain-shortened ones) that barely have any normal laps


def load_data(filter_countries=True):
    lap_times = pd.read_csv(DATA_DIR / "lap_times.csv", na_values="\\N")
    drivers = pd.read_csv(DATA_DIR / "drivers.csv", na_values="\\N")
    races = pd.read_csv(DATA_DIR / "races.csv", na_values="\\N")
    circuits = pd.read_csv(DATA_DIR / "circuits.csv", na_values="\\N")

    races = races[races["year"] == YEAR]
    races = races[races["raceId"].isin(lap_times["raceId"])]  # some races have no lap times recorded

    usable_lap_times = lap_times[lap_times["milliseconds"] / 1000 < MAX_LAP_SECONDS]
    usable_lap_counts = usable_lap_times.groupby("raceId").size()
    races = races[races["raceId"].map(usable_lap_counts).fillna(0) >= MIN_USABLE_LAPS]

    if filter_countries:
        races = races.merge(circuits[["circuitId", "country"]], on="circuitId")
        available_countries = races["country"].unique().tolist()
        chosen_countries = random.sample(available_countries, NUM_RANDOM_COUNTRIES)
        races = races[races["country"].isin(chosen_countries)]
        races = races.drop(columns=["country"])

    lap_times = lap_times[lap_times["raceId"].isin(races["raceId"])]

    return lap_times, drivers, races, circuits


def build_dataframe(lap_times, drivers, races, circuits):
    df = lap_times.merge(drivers[["driverId", "nationality"]], on="driverId")
    df = df.rename(columns={"nationality": "driver_country"})

    df = df.merge(races[["raceId", "circuitId"]], on="raceId")
    df = df.merge(circuits[["circuitId", "country"]], on="circuitId")
    df = df.rename(columns={"country": "race_country"})

    df = df.rename(columns={"milliseconds": "time_ms"})

    df = df[["driver_country", "race_country", "lap", "position", "time_ms"]]

    return df


def plot_lap_times(df):
    df = df.copy()
    df["time_s"] = df["time_ms"] / 1000
    df = df[df["time_s"] < MAX_LAP_SECONDS]

    g = sns.FacetGrid(df, row="driver_country", col="race_country", margin_titles=True)
    g.map(sns.kdeplot, "time_s")

    FIGURES_DIR.mkdir(exist_ok=True)
    g.savefig(FIGURES_DIR / "f1_lap_times_by_country.png")


def main():
    lap_times, drivers, races, circuits = load_data()
    df = build_dataframe(lap_times, drivers, races, circuits)
    plot_lap_times(df)


if __name__ == "__main__":
    main()
