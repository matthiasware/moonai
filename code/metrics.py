import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support


def accuracy(y1, y2):
    y1 = np.array(y1)
    y2 = np.array(y2)
    return (y1 == y2).sum() / y1.size

def soft_acuracy(y1, y2, tol=1):
    y1 = np.array(y1)
    y2 = np.array(y2)
    d = np.abs(y1 - y2)
    return (d <= tol).sum() / d.size

def soft_transform_pred(y_true, y_pred, tol=1):
    idcs = np.abs(y_true - y_pred) <= tol
    y_pred[idcs] = y_true[idcs]
    return y_pred

def soft_classification_report(y_true, y_pred, tol, **kwargs):
    y_pred = soft_transform_pred(y_true.copy(), y_pred.copy(), tol)
    report = classification_report(y_true, y_pred, **kwargs)
    return report

def soft_precision_recall_fscore_support(y_true, y_pred, tol=0):
    y_pred = soft_transform_pred(y_true.copy(), y_pred.copy(), tol)
    return precision_recall_fscore_support(y_true, y_pred)