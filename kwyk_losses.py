#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 09:48:48 2021

@author: hoda
"""

import tensorflow as tf
from tensorflow.python.keras.utils.losses_utils import ReductionV2
from tensorflow.python.keras.losses import LossFunctionWrapper

###### noberainer implementation of elbo loss
def elbo(y_true, y_pred, model, num_examples, from_logits=False):
    """Labels should be integers in `[0, n)`."""
    scc_fn = tf.losses.SparseCategoricalCrossentropy(from_logits=from_logits)
    neg_log_likelihood = -scc_fn(y_true, y_pred)
    kl = sum(model.losses) / num_examples
    elbo_loss = neg_log_likelihood + kl
    return elbo_loss

# ##### implementation that Alice had
# def elbo(y_true, y_pred, model, num_examples, from_logits=False):
#     """Labels should be integers in `[0, n)`."""
#     scc_fn = tf.losses.SparseCategoricalCrossentropy(from_logits=from_logits,reduction=tf.keras.losses.Reduction.NONE)
#     neg_log_likelihood = scc_fn(y_true, y_pred)
#     kl = sum(model.losses) / num_examples
#     elbo_loss = neg_log_likelihood + kl
#     elbo_loss = tf.reduce_sum(elbo_loss)/2
#     return elbo_loss

# ####### Elbo loss implementation from the web
# def elbo(y_true, y_pred, model, num_examples, from_logits=False):
    
#     logit = model(data)# Compute the -ELBO as the loss, averaged over the batch size.
#     labels_distribution = tfp.distributions.Categorical(logits=logits)
#     neg_log_likelihood = -tf.reduce_mean(labels_distribution.log_prob(labels))
#     kl = sum(model.losses) / mnist_conv.train.num_examples
#     elbo_loss = neg_log_likelihood + kl
#     return elbo_loss

# ###### my elbo implementation
# def elbo(label, predictions):
#     # to be implemented
#     elbo_loss = None
#     return elbo_loss


class ELBO(LossFunctionWrapper):
    """Loss to minimize Evidence Lower Bound (ELBO).
    Use this loss for multiclass variational segmentation.
    Labels should not be one-hot encoded.
    """

    def __init__(
        self,
        model,
        num_examples,
        from_logits=False,
        reduction=ReductionV2.AUTO,
        name="ELBO",
    ):
        super().__init__(
            elbo,
            model=model,
            num_examples=num_examples,
            from_logits=from_logits,
            name=name,
            reduction=reduction,
        )

