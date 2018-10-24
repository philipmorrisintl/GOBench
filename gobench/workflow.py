# Copyright (c) 2017 Sylvain Gubian <sylvain.gubian@pmi.com>,
# Yang Xiang <yang.xiang@pmi.com>
# Author: Sylvain Gubian, PMP S.A.
# -*- coding: utf-8 -*-
import os
import sys
import logging
from argparse import RawTextHelpFormatter
from .bench import Benchmarker
from .benchstore import report
import subprocess
import argparse

logger = logging.getLogger(__name__)

DEFAULT_NB_RUNS = 100
DEFAULT_OUTPUT_FOLDER = os.path.join(os.getcwd(), 'DATA')

# Default settings will use the available cores on the local machine
# For high dimension benchmarking, few functions have been selected from
# the set where functions expression can be generalized for dimension n.

def run_bench():
    parser = argparse.ArgumentParser(
        description='Running benchmark and processing results',
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        '--nb-runs',
        dest='nb_runs',
        action='store',
        type=int,
        default=DEFAULT_NB_RUNS,
        help='''
        Number of runs for a given function to test by an algorithm.
        Each run will have a different seed value so that the initial
        coordinates will be a different random location.
        Default value is 100 runs.
        '''
    )
    parser.add_argument(
        '--output-folder',
        dest='output_folder',
        action='store',
        default=DEFAULT_OUTPUT_FOLDER,
        help='''
        Folder where data file for optimization results are stored.
        Default will create a DATA folder in the working directory.
        Note: Using default will make the benchmark running for a long time,
        better to use a cluster infrastructure.
        '''
    )
    parser.add_argument(
        '--functions',
        dest='functions',
        action='store',
        default=None,
        help='''
        Comma separated names of function to be used in the benchmark.
        By default, all testing functions from SciPy benchmark are used.
        Note: Using default will make the benchmark running for a long time,
        better to use a cluster infrastructure.
        '''
    )
    parser.add_argument(
        '--methods',
        dest='methods',
        action='store',
        default=None,
        help='''
        Comma separated names of methods to be benchmarked.
        'DA' for dual annealing
        'BH' for basinhopping
        'DE' for differential evolution
        'DE-R' for differential evolution restart version
        'PSO' for particule swarm
        'PSO-R' for particule swarm restart version
        'BF' for for brute force
        'CMA' for Cov. matrix adaptation evolution strategy
        'CMA-R' for Cov. matrix adaptation evolution strategy restart version
        ''')
    args = parser.parse_args()
    nb_runs = args.nb_runs
    output_folder = args.output_folder
    functions = args.function
    methods = args.methods

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    logger.warning(('The benchmark may take very long time depending on the'
                    ' number of cores available on your machine...'))
    bm = Benchmarker(nb_runs, output_folder, function, methods)
    bm.run()