# Exercise: predicting finishing position from a lap time
#
# We already wrote the parts that are hard to guess:
#   - loading lap_times.csv and turning it into (raceId, time) -> position
#   - splitting the data into a training set and a test set
#   - plotting the confusion matrix
#
# Your job is to complete train_classifier() below (look for TODO).

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "f1db_csv"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"


def load_data():
    # This is given: read lap_times.csv, and turn it into the two inputs
    # our model will use (race_id, time_s) plus the label we want to
    # predict (position).
    lap_times = pd.read_csv(DATA_DIR / "lap_times.csv", na_values="\\N")

    # raceId values are real database IDs (e.g. 841, 842, ...), not a
    # continuous 0, 1, 2, ... range. pandas.factorize() replaces each
    # raceId with a small integer, starting from 0, without changing how
    # many distinct races there are.
    race_id, _ = pd.factorize(lap_times["raceId"])

    time_s = lap_times["milliseconds"] / 1000

    X = pd.DataFrame({"race_id": race_id, "time_s": time_s})
    y = lap_times["position"]

    return X, y


def split_data(X, y, test_size=0.2, random_state=0):
    # This is given: a random split into a training set and a test set.
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_classifier(X_train, y_train):
    # TODO (your part):
    # 1. Instantiate a classification model. Any classifier from sklearn
    #    works (see the "Machine Learning Models" slides) - for example:
    #        from sklearn.neighbors import KNeighborsClassifier
    #        model = KNeighborsClassifier(n_neighbors=25)
    # 2. Train it on the training data with model.fit(X_train, y_train).
    # 3. Return the trained model.
    pass  # <- remove this line once you add your code


def plot_confusion_matrix(model, X_test, y_test):
    # This is given: plot the confusion matrix of the trained model over
    # the test set, and save it instead of opening a window.
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap="Blues", colorbar=False)

    FIGURES_DIR.mkdir(exist_ok=True)
    plt.gcf().set_size_inches(10, 10)
    plt.title("Predicting finishing position from (race, lap time)")
    plt.savefig(FIGURES_DIR / "f1_position_confusion_matrix.png", bbox_inches="tight")


if __name__ == "__main__":
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    model = train_classifier(X_train, y_train)
    plot_confusion_matrix(model, X_test, y_test)

