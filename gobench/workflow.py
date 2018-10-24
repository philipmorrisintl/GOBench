# Copyright (c) 2017 Sylvain Gubian <sylvain.gubian@pmi.com>,
# Yang Xiang <yang.xiang@pmi.com>
# Author: Sylvain Gubian, PMP S.A.
# -*- coding: utf-8 -*-
import os
import sys
import logging
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

def run_all_bench():
    parser = argparse.ArgumentParser(
        description='Running benchmark and processing results')
    parser.add_argument(
        '--nb-runs',
        dest='nb_runs',
        action='store',
        type=int,
        default=DEFAULT_NB_RUNS,
        help='Number of runs for a given function to test by an algorithm'
    )
    parser.add_argument(
        '--output-folder',
        dest='output_folder',
        action='store',
        default=DEFAULT_OUTPUT_FOLDER,
        help='Folder where data file for optimization results are stored',
    )
    args = parser.parse_args()
    nb_runs = args.nb_runs
    output_folder = args.output_folder

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    logger.warning(('The benchmark may take very long time depending on the'
                    ' number of cores available on your machine...'))
    bm = Benchmarker(nb_runs, output_folder)
    bm.run()
