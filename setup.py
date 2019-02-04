import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'numpy==1.15.2',
    'scipy==1.2.0',
    'pyswarm==0.6',
    'matplotlib',
    'fastcluster',
    'cma==2.6.0',
    #'nlopt',
    'pandas',
    ]

setup(
        name='GOBench',
        version='0.0.1',
        description='Global optimization benchmark',
        long_description=README + '\n\n' +  CHANGES,
        classifiers=[
            "Programming Language :: Python",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering :: Mathematics",
          ],
        author='Sylvain Gubian, PMP SA',
        author_email='sylvain.gubian@pmi.com',
        url='https://github.com/sgubianpm/gobench',
        keywords='global optimization benchmarking',
        packages=find_packages(),
        include_package_data=True,
        entry_points = {
            'console_scripts':
            [
                'gobench=gobench.workflow:run_bench',
                'goreport=gobench.workflow:report',
                'gofuncdim=gobench.bench:get_func_default_dim',
            ],
        },
        install_requires=requires,
      )
