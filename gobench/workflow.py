# Copyright (c) 2017 Sylvain Gubian <sylvain.gubian@pmi.com>,
# Yang Xiang <yang.xiang@pmi.com>
# Author: Sylvain Gubian, PMP S.A.
# -*- coding: utf-8 -*-
import os
import sys
import logging
import argparse
from argparse import RawTextHelpFormatter
from .bench import Benchmarker
from .benchstore import process_results
from .plots import heatmap_reliability
from .plots import barplot
from .plots import all_func_nb_call

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
        'CMA-R' for Cov. matrix adaptation evolution strategy restart version.
        If not provided, all of these methods are benchmarked.
        ''')
    args = parser.parse_args()
    nb_runs = args.nb_runs
    output_folder = args.output_folder
    functions = args.functions
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
    bm = Benchmarker(nb_runs, output_folder, functions, methods)
    bm.run()

def report():
    parser = argparse.ArgumentParser(
        description='Generate reports with benchmark results',
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        '--results-folder',
        dest='results_folder',
        action='store',
        default=DEFAULT_OUTPUT_FOLDER,
        help='''
        Folder where data file for optimization results are stored.
        '''
    )
    parser.add_argument(
        '--out',
        dest='output_filepath',
        action='store',
        default=None,
        help='''
        Path for the figure file to be generated. The given file extention
        will set the file format to be generated (pdf, png, svg, eps, or csv
        for tabular results)
        '''
    )
    parser.add_argument(
        '--type',
        dest='result_type',
        action='store',
        default='heatmap',
        help='''
        Type of report to be generated. Possible reports are for now:
        heatmap, csv.
        ''')
    args = parser.parse_args()
    results_folder = args.results_folder
    output_file = args.output_filepath
    result_type = args.result_type

    if results_folder is None:
        results_folder = DEFAULT_OUTPUT_FOLDER

    if result_type == 'heatmap':
        data = process_results(results_folder, kind='raw')
        heatmap_reliability(data, output_file)
    else:
        process_results(results_folder, kind='csv', path=output_file)
