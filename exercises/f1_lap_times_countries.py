# Exercise: from IDs to countries
#
# We already wrote the parts that are hard to guess:
#   - loading the CSV files
#   - keeping only one season, so the plot stays fast and readable
#   - the seaborn plot itself
#
# Your job is to complete build_dataframe() below (look for TODO).
#
# This is the same idea as the seaborn "iris" example:
#   https://seaborn.pydata.org/tutorial/axis_grids.html
#
#   g = sns.PairGrid(iris, hue="species")
#   g.map_diag(sns.histplot)
#   g.map_offdiag(sns.scatterplot)
#   g.add_legend()
#
# Each grid cell here is one (driver_country, race_country) pair:
# rows are the driver's country, columns are the race's country, and
# every cell shows a KDE of the lap times for that pair.

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
    # This is given: read the CSV files we need, and keep only the
    # laps raced during YEAR (there are ~500,000 laps in total across
    # every season - way too many points to plot at once).
    lap_times = pd.read_csv(DATA_DIR / "lap_times.csv", na_values="\\N")
    drivers = pd.read_csv(DATA_DIR / "drivers.csv", na_values="\\N")
    races = pd.read_csv(DATA_DIR / "races.csv", na_values="\\N")
    circuits = pd.read_csv(DATA_DIR / "circuits.csv", na_values="\\N")

    races = races[races["year"] == YEAR]
    races = races[races["raceId"].isin(lap_times["raceId"])]  # some races have no lap times recorded

    # keep only races with enough usable (non-outlier) laps, so a
    # race that never really got going doesn't sneak into the sample
    usable_lap_times = lap_times[lap_times["milliseconds"] / 1000 < MAX_LAP_SECONDS]
    usable_lap_counts = usable_lap_times.groupby("raceId").size()
    races = races[races["raceId"].map(usable_lap_counts).fillna(0) >= MIN_USABLE_LAPS]

    # if filter_countries is True, keep only NUM_RANDOM_COUNTRIES
    # random race countries, so the grid stays small; if False, use
    # every race of the season.
    if filter_countries:
        races = races.merge(circuits[["circuitId", "country"]], on="circuitId")
        available_countries = races["country"].unique().tolist()
        chosen_countries = random.sample(available_countries, NUM_RANDOM_COUNTRIES)
        races = races[races["country"].isin(chosen_countries)]
        races = races.drop(columns=["country"])

    lap_times = lap_times[lap_times["raceId"].isin(races["raceId"])]

    return lap_times, drivers, races, circuits


def build_dataframe(lap_times, drivers, races, circuits):
    # TODO (your part):
    # Starting from lap_times, build a new DataFrame where:
    #
    # 1. driverId is replaced by the driver's nationality, in a new
    #    column called "driver_country".
    #    Hint: drivers has one row per driverId, with a "nationality"
    #    column. Merge lap_times with drivers on "driverId"
    #    (pandas.merge), then rename "nationality" to "driver_country".
    #
    # 2. raceId is replaced by the race's country, in a new column
    #    called "race_country".
    #    Hint: races has one row per raceId, with a "circuitId"
    #    column; circuits has one row per circuitId, with a "country"
    #    column. So you need two merges: lap_times -> races (on
    #    "raceId") to pick up "circuitId", then -> circuits (on
    #    "circuitId") to pick up "country". Rename "country" to
    #    "race_country".
    #
    # 3. The lap time itself is kept as "time_ms": rename the
    #    "milliseconds" column from lap_times to "time_ms".
    #
    # 4. Every other column is dropped (driverId, raceId, circuitId,
    #    and anything else the merges picked up along the way).
    #
    # The DataFrame you return must have exactly these columns:
    #   driver_country, race_country, lap, position, time_ms
    pass  # <- remove this line once you add your code


def plot_lap_times(df):
    # This is given: convert milliseconds to seconds (nicer numbers),
    # and drop the handful of laps affected by a safety car or red
    # flag - real races have those, and they show up as much longer
    # than a normal lap, not as measurement errors.
    df = df.copy()
    df["time_s"] = df["time_ms"] / 1000
    df = df[df["time_s"] < MAX_LAP_SECONDS]

    # One grid cell per (driver_country, race_country) pair, every
    # cell showing a KDE of the lap times for that pair.
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
