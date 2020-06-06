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
    all_evidence = []
    labels = []

    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            evidence = []
            # Append list of evidence per row
            # - Administrative, an integer
            evidence.append(row[0])
            # - Administrative_Duration, a floating point number
            evidence.append(float(row[1]))
            # - Informational, an integer
            evidence.append(row[2])
            # - Informational_Duration, a floating point number
            evidence.append(float(row[3]))
            # - ProductRelated, an integer
            evidence.append(row[4])
            # - ProductRelated_Duration, a floating point number
            evidence.append(float(row[5]))
            # - BounceRates, a floating point number
            evidence.append(float(row[6]))
            # - ExitRates, a floating point number
            evidence.append(float(row[7]))
            # - PageValues, a floating point number
            evidence.append(float(row[8]))
            # - SpecialDay, a floating point number
            evidence.append(float(row[9]))
            # - Month, an index from 0 (January) to 11 (December)
            evidence.append(monthToNum(row[10]))
            # - OperatingSystems, an integer
            evidence.append(row[11])
            # - Browser, an integer
            evidence.append(row[12])
            # - Region, an integer
            evidence.append(row[13])
            # - TrafficType, an integer
            evidence.append(row[14])
            # - VisitorType, an integer 0 (not returning) or 1 (returning)
            if row[15] == "Returning_Visitor":
                evidence.append(1)
            else:
                evidence.append(0)
            # - Weekend, an integer 0 (if false) or 1 (if true)   
            if row[16] == "TRUE":
                evidence.append(1)
            else:
                evidence.append(0)
            # Append list of evidence to all_evidence
            all_evidence.append(evidence)

            # Append label
            if row[17] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)

    return (all_evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    true_correct = 0.0
    true_count = 0.0
    false_correct = 0.0
    false_count = 0.0

    for i in range(len(labels)):
        # If label == True
        if labels[i] == 1:
            true_count += 1
            if labels[i] == predictions[i]:
                true_correct += 1
        # If label == False
        if labels[i] == 0:
            false_count += 1
            if labels[i] == predictions[i]:
                false_correct += 1
    
    sensitivity = true_correct / true_count
    specificity = false_correct / false_count

    return (sensitivity, specificity)


def monthToNum(shortMonth):
    return{
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'June': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11
    }[shortMonth]


if __name__ == "__main__":
    main()
