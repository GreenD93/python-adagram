#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import argparse
import logging

from .model import VectorModel, Dictionary


def main():
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('input', help='training text data (tokenized)')
    arg('output', help='output file to save the model')
    arg('--dict', help='dictionary file with word frequencies')
    arg('--window', help='window (or half-context) size', type=int, default=4)
    arg('--min-freq', help='min. frequency of words', type=int, default=10)
    arg('--dim', help='dimensionality of representations', type=int, default=100)
    arg('--prototypes', help='max. number of word prototypes', type=int, default=5)
    arg('--sense-threshold',
        help='minimal probability of a meaning to contribute into gradients',
        type=float, default=1e-10)
    arg('--alpha', help='prior probability of allocating a new prototype',
        type=float, default=0.1)
    arg('--context-cut', help='randomly reduce size of the context',
        action='store_true')
    arg('--epochs', help='number of epochs to train', type=int, default=1)
    arg('--workers', help='number of workers (one by default)',
        type=int, default=1)

    args = parser.parse_args()

    logging.basicConfig(
        format='[%(levelname)s] %(asctime)s %(message)s',
        level=logging.INFO)
    if args.dict:
        logging.info('Reading dictionary...')
        dictionary = Dictionary.read(args.dict, min_freq=args.min_freq)
    else:
        logging.info('Building dictionary...')
        dictionary = Dictionary.build(args.input, min_freq=args.min_freq)
    logging.info('Done! {} words.'.format(len(dictionary)))

    vm = VectorModel(dictionary=dictionary, dim=args.dim,
                     prototypes=args.prototypes, alpha=args.alpha)
    vm.train(args.input, args.window,
             context_cut=args.context_cut, sense_threshold=args.sense_threshold,
             epochs=args.epochs, n_workers=args.workers)
    vm.save(args.output)
