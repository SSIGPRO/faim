# Solution: predicting finishing position from a lap time
#
# Same as f1_position_classifier.py, but with train_classifier() filled in.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "f1db_csv"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"


def load_data():
    lap_times = pd.read_csv(DATA_DIR / "lap_times.csv", na_values="\\N")

    race_id, _ = pd.factorize(lap_times["raceId"])
    time_s = lap_times["milliseconds"] / 1000

    X = pd.DataFrame({"race_id": race_id, "time_s": time_s})
    y = lap_times["position"]

    return X, y


def split_data(X, y, test_size=0.2, random_state=0):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_classifier(X_train, y_train):
    model = KNeighborsClassifier(n_neighbors=25)
    model.fit(X_train, y_train)
    return model


def plot_confusion_matrix(model, X_test, y_test):
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap="Blues", colorbar=False)

    FIGURES_DIR.mkdir(exist_ok=True)
    plt.gcf().set_size_inches(10, 10)
    plt.title("Predicting finishing position from (race, lap time)")
    plt.savefig(FIGURES_DIR / "f1_position_confusion_matrix.png", bbox_inches="tight")


def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    model = train_classifier(X_train, y_train)
    plot_confusion_matrix(model, X_test, y_test)


if __name__ == "__main__":
    main()
