from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

def evaluate_thresholds(model, X_test, y_test):

    probs = model.predict_proba(X_test)[:, 1]

    for threshold in [0.3, 0.4, 0.5, 0.6, 0.7]:
        print("\n==============================")
        print(f"Threshold: {threshold}")

        y_pred = (probs >= threshold).astype(int)

        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))