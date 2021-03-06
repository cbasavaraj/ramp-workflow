"""Multiclass predictions.

``y_pred`` should be two dimensional (n_samples x n_classes).

"""

# Author: Balazs Kegl <balazs.kegl@gmail.com>
# License: BSD 3 clause

import numpy as np
from .base import BasePrediction


def _multiclass_init(self, y_pred=None, y_true=None, n_samples=None):
    if y_pred is not None:
        self.y_pred = np.array(y_pred)
    elif y_true is not None:
        self._init_from_pred_labels(y_true)
    elif n_samples is not None:
        self.y_pred = np.empty((n_samples, self.n_columns), dtype=float)
        self.y_pred.fill(np.nan)
    else:
        raise ValueError(
            'Missing init argument: y_pred, y_true, or n_samples')
    self.check_y_pred_dimensions()


def _init_from_pred_labels(self, y_pred_labels):
    """Initalize y_pred to uniform for (positive) labels in y_pred_labels.

    Initialize multiclass Predictions from ground truth. y_pred_labels
    can be a single (positive) label in which case the corresponding
    column gets probability of 1.0. In the case of multilabel (k > 1
    positive labels), the columns corresponing the positive labels
    get probabilities 1/k.

    Parameters
    ----------
    y_pred_labels : list of objects or list of list of objects
        (of the same type)
    """
    type_of_label = type(self.label_names[0])
    self.y_pred = np.zeros(
        (len(y_pred_labels), len(self.label_names)), dtype=np.float64)
    for ps_i, label_list in zip(self.y_pred, y_pred_labels):
        # converting single labels to list of labels, assumed below
        if type(label_list) != np.ndarray and type(label_list) != list:
            label_list = [label_list]
        label_list = list(map(type_of_label, label_list))
        for label in label_list:
            ps_i[self.label_names.index(label)] = 1.0 / len(label_list)


@property
def _y_pred_label_index(self):
    """Multi-class y_pred is the index of the predicted label."""
    return np.argmax(self.y_pred, axis=1)


@property
def _y_pred_label(self):
    return self.label_names[self.y_pred_label_index]


def make_multiclass(label_names=[]):
    Predictions = type(
        'Predictions',
        (BasePrediction,),
        {'label_names': label_names,
         'n_columns': len(label_names),
         # Multiclass ground truth is a 1D vector of labels
         'n_columns_true': 0,
         '__init__': _multiclass_init,
         '_init_from_pred_labels': _init_from_pred_labels,
         'y_pred_label_index': _y_pred_label_index,
         'y_pred_label': _y_pred_label,
         })
    return Predictions
