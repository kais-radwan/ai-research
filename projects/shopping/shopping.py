import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def read_bool(value: str) -> int:
    if str.lower(value) == "true":
        return 1

    return 0


def read_month(value: str) -> int:
    months = [
        'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',
        'aug', 'sep', 'oct', 'nov', 'dec'
    ]

    value = str.lower(value)[:3]
    index = months.index(value)

    return index


def read_visitor(value: str) -> int:
    value = str.lower(value)

    if str.startswith(value, "return"):
        return 1

    return 0


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            l = read_bool(row["Revenue"])
            labels.append(l)

            evidence.append([
                float(row["Administrative"]), float(row["Administrative_Duration"]), 
                float(row["Informational"]), float(row["Informational_Duration"]), 
                float(row["ProductRelated"]), float(row["ProductRelated_Duration"]),
                float(row["BounceRates"]), float(row["ExitRates"]), 
                float(row["PageValues"]), float(row["SpecialDay"]),
                read_month(row["Month"]), float(row["OperatingSystems"]),
                float(row["Browser"]), float(row["Region"]),
                float(row["TrafficType"]), read_visitor(row["VisitorType"]),
                read_bool(row["Weekend"])
            ])

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    classifier = KNeighborsClassifier(1)
    classifier.fit(evidence, labels)

    return classifier


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sens = []
    spec = []

    for i in range(len(labels)):
        l = labels[i]
        p = predictions[i]

        if l == 1 and l == p:
            sens.append(1)
            continue
        elif l == 1:
            sens.append(0)
            continue

        if l == 0 and l == p:
            spec.append(1)
            continue
        elif l == 0:
            spec.append(0)

    t_sens = [t for t in sens if t == 1]
    sens = len(t_sens) / len(sens)

    t_spec = [t for t in spec if t == 1]
    spec = len(t_spec) / len(spec)

    return (sens, spec)


if __name__ == "__main__":
    main()
