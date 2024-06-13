"""Copyright 2022 by Artem Ustsov"""

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import f1_score, roc_curve, confusion_matrix
import numpy as np
import os


def plot_roc_curve(true_y: np.array, y_prob: np.array, output_path: str):
    """Plots the roc curve based of the probabilities"""

    fig = plt.figure(figsize=(5, 5))
    fpr, tpr, thresholds = roc_curve(true_y, y_prob)

    plt.title(f"ROC CURVE with f1-score: {f1_score(true_y, y_prob):.3f}")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.grid(True)
    plt.plot(fpr, tpr)

    obj_path = os.path.join(output_path, "roc_auc_curve.png")
    fig.savefig(obj_path)
    plt.close(fig)
    return obj_path


def plot_confusion_matrix(
    true_y: np.array, y_prob: np.array, output_path: str
):
    """Plots the roc curve based of the probabilities"""

    fig = plt.figure(figsize=(7, 5))

    sns.heatmap(
        confusion_matrix(true_y, y_prob, normalize="all"),
        annot=True,
        fmt=".2%",
        cmap="YlGnBu",
    )
    plt.plot()
    obj_path = os.path.join(output_path, "confusion_matrix.png")
    fig.savefig(obj_path)
    plt.close(fig)
    return obj_path
